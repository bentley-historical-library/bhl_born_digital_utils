import argparse
import csv
import os

parser = argparse.ArgumentParser(description='Check missing folders')
parser.add_argument('--src', required=True, help='Target directory')
args = parser.parse_args()


# Function
# Parsing barcodes (with a successful transfer) from bhl_inventory.csv
def parse_barcodes(src_path):
    with open(os.path.join(src_path, 'bhl_inventory.csv'), mode='r') as bhl_inventory_csv_file:
        csv_reader = csv.DictReader(bhl_inventory_csv_file)
        for row in csv_reader:
            # For Jackie bhl_inventory
            if 'pass_1_successful?' in row:
                if row['pass_1_successful?'] == 'Y' or row['pass_2_successful?'] == 'Y':
                    csv_list.append(row['barcode'].rstrip())

            # For RMW bhl_inventory
            if 'pass_successful?' in row:
                if row['pass_successful?'] == 'Y':
                    csv_list.append(row['barcode'].rstrip())

    print('Found', len(csv_list), 'barcodes in bhl_inventory.csv file.')


# Parsing barcode directories in src
def parse_directories(src_path):
    for directory in os.listdir(src_path):
        if os.path.isdir(os.path.join(src_path, directory)):
            directory_list.append(directory.rstrip())

    print('Found', len(directory_list), 'folders in', src_path + '.')


# Cross-comparing two lists
def compare_lists(src_path):
    # Pass A, do barcodes from csv_list in directory_list?
    for barcode in csv_list:
        duplicate_barcode = '_' + barcode
        if barcode not in directory_list and duplicate_barcode not in directory_list:
            missing_list_A.append(barcode)

    print('Found', len(missing_list_A), 'barcodes not in', src_path + '.')

    for barcode in missing_list_A:
        print(barcode, "is missing.")

    # Pass B, do barcodes from directory_list in csv_list?
    for barcode in directory_list:
        if barcode.strip('_') not in csv_list:
            missing_list_B.append(barcode)

    print('Found', len(missing_list_B), 'folders not in', 'bhl_inventory.csv.')

    for barcode in missing_list_B:
        print(barcode, "is missing.")


# Script
csv_list = []
directory_list = []
missing_list_A = []
missing_list_B = []

print('Checking missing folders in', args.src)

parse_barcodes(args.src)
parse_directories(args.src)
compare_lists(args.src)
