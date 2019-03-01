import argparse
import csv
import os

parser = argparse.ArgumentParser(description='Check missing folders')
parser.add_argument('-i', '--input', required=True, help='Input directory')
args = parser.parse_args()


# Function
# Parsing barcodes (with a successful transfer) from bhl_inventory.csv
def parse_barcodes(src_path):
    with open(os.path.join(src_path, 'bhl_inventory.csv'), mode='r') as bhl_inventory_csv_file:
        csv_reader = csv.DictReader(bhl_inventory_csv_file)
        for row in csv_reader:
            if row['separation'] == 'Y':
                csv_fail_list.append(row['barcode'].rstrip(' '))
            elif row['separation'] == 'N':
                if row['pass_1_successful'] == 'Y' or row['pass_2_successful'] == 'Y':
                    csv_pass_list.append(row['barcode'].rstrip(' '))

    print('Found', len(csv_fail_list) + len(csv_pass_list), 'barcodes,',
          len(csv_pass_list), 'passed and', len(csv_fail_list), 'failed, barcodes in bhl_inventory.csv file.')


# Parsing barcode directories in src
def parse_directories(src_path):
    for directory in os.listdir(src_path):
        if os.path.isdir(os.path.join(src_path, directory)):
            if directory.startswith('_'):
                directory_fail_list.append(directory.lstrip('_').rstrip(' '))
            else:
                directory_pass_list.append(directory.rstrip(' '))

    print('Found', len(directory_fail_list) + len(directory_pass_list), 'folders',
          len(directory_pass_list), 'passed and', len(directory_fail_list), 'failed, in', src_path + '.')


# Cross-comparing two lists
def compare_lists(src_path):
    # Pass A, do barcodes from csv_list in directory_list?
    for barcode in csv_pass_list:
        if barcode not in directory_pass_list:
            missing_list_A.append(barcode)

    for barcode in csv_fail_list:
        if barcode not in directory_fail_list:
            missing_list_A.append(barcode)

    print('Found', len(missing_list_A), 'barcodes not in', src_path + '.')

    for barcode in missing_list_A:
        print(barcode, "is missing.")

    # Pass B, do barcodes from directory_list in csv_list?
    for barcode in directory_pass_list:
        if barcode not in csv_pass_list:
            missing_list_B.append(barcode)

    for barcode in directory_fail_list:
        if barcode not in csv_fail_list:
            missing_list_B.append(barcode)

    print('Found', len(missing_list_B), 'folders not in', 'bhl_inventory.csv.')

    for barcode in missing_list_B:
        print(barcode, 'is missing.')


# Script
csv_pass_list = []
csv_fail_list = []
directory_pass_list = []
directory_fail_list = []
missing_list_A = []
missing_list_B = []

print('Checking missing folders in', args.input)

parse_barcodes(args.input)
parse_directories(args.input)
compare_lists(args.input)
