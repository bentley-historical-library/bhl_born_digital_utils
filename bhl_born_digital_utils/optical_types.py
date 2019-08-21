import argparse
import csv
import os
from subprocess import call

##### Running this script #####
# <drive letter>: <enter> [If script located in different drive.]
# cd <script/folder/path> <enter>
# python optical_types.py -i <inventory>.csv -o <directory/containing/barcode/folders> <enter>

parser = argparse.ArgumentParser(description='Filtering A/V & separation barcodes from the inventory spreadsheet.')
parser.add_argument('-i', '--input', required=True, help='Input directory')
parser.add_argument('-o', '--output', required=True, help='Scanning directory')
args = parser.parse_args()

def get_target(csv_sheet):

    temp_list = []  # list of CSV rows [dictionaries]
    return_list = []  # list of barcodes

    with open(csv_sheet, mode='r') as inventory:
        csv_reader = csv.DictReader(inventory)
        csv_reader.fieldnames = [fieldname.strip().lower() for fieldname in csv_reader.fieldnames]

        # Removing non-targets, rows that are audio CD or video DVD
        for row in csv_reader:
            if row['media_type'] == 'data CD' or row['media_type'] == 'data DVD':
                temp_list.append(dict(row))

        # Removing non-targets, rows that are separation
        for row in csv_reader:
            if row['separation'] == 'Y':
                temp_list.remove(row)

        # Removing non-targets, rows without barcodes
        for row in csv_reader:
            if len(row['barcode']) != 14:
                temp_list.remove(row)

        # Additional filtering, only adding successful transfers w/o DIPs
        for row in temp_list:
            if row['pass_1_successful'] == 'Y' and row['made_dip'] == 'N/A':
                return_list.append(row['barcode'])

            if row['pass_1_successful'] == 'N' and row['pass_2_successful'] == 'Y' and row['made_dip'] == 'N/A':
                return_list.append(row['barcode'])

    return return_list

def copy_barcodes(return_list, scan_path):
    folder_list = []
    separations = []  # print this out if you want to double check what will be separated

    # Checking if the file path exists before trying to copy content.
    for barcode in return_list:
        scan_dir_path = os.path.join(scan_path, str(barcode))
        check_path = os.path.exists(scan_dir_path)
        if check_path == True:
            folder_list.append(scan_dir_path)
        else:
            if check_path != True:
                separations.append(scan_dir_path)

    # DUPLICATING the files into the current working directory
    for folders in folder_list:
        barcode_copy = folders[-14:] + '_copy'
            # Creating the copied folder's name to avoid confusion.
        print("Copying folder " + folders + " to the temporary location.")
        call(["robocopy", folders, barcode_copy, "/e", "/tee"])

    return folder_list


target_list = get_target(args.input)

copy_list = copy_barcodes(target_list, args.output)
