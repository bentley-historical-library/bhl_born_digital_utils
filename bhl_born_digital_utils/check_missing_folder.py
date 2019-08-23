import csv
import os
import sys


def print_findings(findings, name, location, report_type="count"):
    passed = len(findings["pass"])
    failed = len(findings["fail"])
    total = passed + failed
    print("\nFound {} total {} in {}".format(total, name, location))
    if report_type == "count":
        print("\nPASSED: {}".format(passed))
        print("\nFAILED: {}".format(failed))
    elif report_type == "list":
        print("\nPASSED:")
        for entry in findings["pass"]:
            print(entry)
        print("\nFAILED:")
        for entry in findings["fail"]:
            print(entry)


def parse_barcodes(bhl_inventory):
    barcodes = {"pass": [], "fail": []}
    with open(bhl_inventory, "r", newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            barcode = row.get("barcode").strip()
            separation = row.get("separation").lower().strip()
            pass_1 = row.get("pass_1_successful").lower().strip()
            pass_2 = row.get("pass_2_successful").lower().strip()
            if separation in ["y", "yes"]:
                barcodes["fail"].append(barcode)
            elif pass_1 in ["y", "yes"] or pass_2 in ["y", "yes"]:
                barcodes["pass"].append(barcode)
    print_findings(barcodes, "barcodes", bhl_inventory, report_type="count")
    return barcodes


def parse_directories(src_path):
    directories = {"pass": [], "fail": []}
    for directory in os.listdir(src_path):
        if os.path.isdir(os.path.join(src_path, directory)):
            if directory.startswith("_"):
                directories["fail"].append(directory.lstrip("_").strip())
            else:
                directories["pass"].append(directory.strip())
    print_findings(directories, "directories", src_path, report_type="count")
    return directories


def compare_dicts(a, b, key):
    return [item for item in a[key] if item not in b[key]]


def compare_barcodes_and_directories(src_path, barcodes, directories):
    missing_barcodes = {}
    missing_barcodes["pass"] = compare_dicts(barcodes, directories, "pass")
    missing_barcodes["fail"] = compare_dicts(barcodes, directories, "fail")
    print_findings(missing_barcodes, "missing barcodes", src_path, report_type="list")

    missing_directories = {}
    missing_directories["pass"] = compare_dicts(directories, barcodes, "pass")
    missing_directories["fail"] = compare_dicts(directories, barcodes, "fail")
    print_findings(missing_directories, "missing directories", "bhl_inventory.csv", report_type="list")


def check_missing_folder(src_path):
    print("Checking for missing folders in {}".format(src_path))
    bhl_inventory = os.path.join(src_path, "bhl_inventory.csv")
    if not os.path.exists(bhl_inventory):
        print("bhl_inventory not found at {}".format(bhl_inventory))
        sys.exit()
    barcodes = parse_barcodes(bhl_inventory)
    directories = parse_directories(src_path)
    compare_barcodes_and_directories(src_path, barcodes, directories)
