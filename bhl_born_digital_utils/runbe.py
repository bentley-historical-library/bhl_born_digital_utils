import csv
import os
import shutil
import subprocess

from bhl_born_digital_utils.config import get_config_setting


def get_bulk_extractor_command(source, output):
    be_path = get_config_setting("bulk_extractor", default="bulk_extractor")
    command = [
            be_path, "-S ssn_mode=1", 
            "-E", "accts", "-x", "exif",
            "-o", output, "-R", source
            ]
    return command


def successful(entry):
    return entry.lower().strip() in ["y", "yes"]


def is_target(row):
    separation = row.get("separation")
    made_dip = row.get("made_dip")
    barcode = row.get("barcode").strip()
    pass_1 = row.get("pass_1_successful")
    pass_2 = row.get("pass_2_successful")
    media_type = row.get("media_type")
    if successful(separation):
        return False
    elif successful(made_dip):
        return False
    elif not (successful(pass_1) or successful(pass_2)):
        return False
    elif len(barcode) != 14:
        return False
    elif media_type.startswith("audio") or media_type.startswith("video"):
        return False
    else:
        return True


def get_targets(src):
    bhl_inventory = os.path.join(src, "bhl_inventory.csv")
    targets = []
    with open(bhl_inventory, "r", newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            if is_target(row):
                targets.append(row["barcode"].strip())
    return targets


def parse_results(be_logs_dir):
    for barcode in os.listdir(be_logs_dir):
        barcode_path = os.path.join(be_logs_dir, barcode)
        for filename in os.listdir(barcode_path):
            filepath = os.path.join(barcode_path, filename)
            if os.path.getsize(filepath) == 0 or filename == "report.xml":
                os.remove(filepath)

        if len(os.listdir(barcode_path)) == 0:
            shutil.rmtree(barcode_path)

    if len(os.listdir(be_logs_dir)) == 0:
        print("No bulk_extractor results found.")
        shutil.rmtree(be_logs_dir)
    else:
        print("bulk_extractor results found for the following items:")
        for barcode in os.listdir(be_logs_dir):
            print(barcode)
        print("Check the results for each item in {}".format(be_logs_dir))


def run_bulk_extractor(src, logs_dir):
    accession_number = os.path.split(src)[-1]
    if not os.path.exists(logs_dir):
        os.mkdir(logs_dir)
    accession_dir = os.path.join(logs_dir, accession_number)
    if not os.path.exists(accession_dir):
        os.mkdir(accession_dir)
    be_logs_dir = os.path.join(accession_dir, "bulk_extractor")
    if not os.path.exists(be_logs_dir):
        os.mkdir(be_logs_dir)
    targets = get_targets(src)
    for target in targets:
        source = os.path.join(src, target)
        output = os.path.join(be_logs_dir, target)
        command = get_bulk_extractor_command(source, output)
        subprocess.call(command)
    parse_results(be_logs_dir)
