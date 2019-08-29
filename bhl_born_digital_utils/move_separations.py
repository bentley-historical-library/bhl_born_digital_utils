import csv
import os
import shutil


def move_separations(src_path, dst_path, accession_number):
    bhl_inventory = os.path.join(src_path, "bhl_inventory.csv")
    targets = get_targets(src_path, bhl_inventory)
    if accession_number:
        accession = accession_number
    else:
        accession = os.path.split(src_path)[-1]
    dst_dir = os.path.join(dst_path, "{}_separations".format(accession))
    if not os.path.exists(dst_dir):
        os.mkdir(dst_dir)
    for target in targets:
        shutil.move(target, dst_dir)
        print("{} moved to {}".format(target, dst_dir))


def get_targets(src_path, bhl_inventory):
    targets = []
    with open(bhl_inventory, "r", newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            separation = row.get("separation", "").lower().strip()
            if separation in ["y", "yes"]:
                barcode = row["barcode"].strip()
                separation_barcode = "_{}".format(barcode)
                separation_path = os.path.join(src_path, separation_barcode)
                if not os.path.exists(separation_path):
                    print("Separation directory not found: {}".format(separation_path))
                else:
                    targets.append(separation_path)
    return targets
