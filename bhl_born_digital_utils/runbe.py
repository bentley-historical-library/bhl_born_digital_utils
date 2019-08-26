import csv
import os
import platform
import shutil
import subprocess


def get_bulk_extractor_command(source, output):
    if "windows" in platform.platform().lower():
        be_exe = r"C:\BHL\Utilities\Bulk Extractor 1.6.0-dev\bulk_extractor.exe"
    else:
        be_exe = "bulk_extractor"
    command = [
            be_exe, "-S ssn_mode=1", 
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


def parse_results(output):
    for filename in os.listdir(output):
        filepath = os.path.join(output, filename)
        if os.path.getsize(filepath) == 0 or filename == "report.xml":
            os.remove(filepath)

    if len(os.listdir(output)) == 0:
        shutil.rmtree(output)


def run_bulk_extractor(src):
    base_dir = os.path.dirname(os.path.dirname(__file__))
    logs_dir = os.path.join(base_dir, "logs", "bulk_extractor")
    if not os.path.exists(logs_dir):
        os.mkdir(logs_dir)
    accession_number = os.path.split(src)[-1]
    accession_dir = os.path.join(logs_dir, accession_number)
    if not os.path.exists(accession_dir):
        os.mkdir(accession_dir)
    targets = get_targets(src)
    for target in targets:
        source = os.path.join(src, target)
        output = os.path.join(accession_dir, target)
        command = get_bulk_extractor_command(source, output)
        subprocess.call(command)
        parse_results(output)
