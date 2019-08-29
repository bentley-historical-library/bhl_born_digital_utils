import csv
import os
import shutil


def separate_av_media(src_path, accession_number):
    bhl_inventory = os.path.join(src_path, "bhl_inventory.csv")
    targets = get_targets(src_path, bhl_inventory)
    base_dir = os.path.dirname(src_path)
    if accession_number:
        accession = accession_number
    else:
        accession = os.path.split(src_path)[-1]
    dst_dir = "{}_audiovisual".format(accession)
    dst_dirpath = os.path.join(base_dir, dst_dir)
    if not os.path.exists(dst_dirpath):
        os.mkdir(dst_dirpath)
    for target in targets:
        shutil.move(target, dst_dirpath)
        print("{} moved to {}".format(target, dst_dirpath))


def get_targets(src_path, bhl_inventory):
    targets = []
    with open(bhl_inventory, "r", newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            media_type = row.get("media_type", "").lower().strip()
            if media_type.startswith("audio") or media_type.startswith("video"):
                separation = row.get("separation").lower().strip()
                pass_1 = row.get("pass_1_successful", "").lower().strip()
                pass_2 = row.get("pass_2_successful", "").lower().strip()
                if (pass_1 in ["y", "yes"] or pass_2 in ["y", "yes"]) and separation not in ["y", "yes"]:
                    barcode = row["barcode"].strip()
                    barcode_path = os.path.join(src_path, barcode)
                    if not os.path.exists(barcode_path):
                        print("Barcode directory not found: {}".format(barcode_path))
                    else:
                        targets.append(barcode_path)
    return targets
