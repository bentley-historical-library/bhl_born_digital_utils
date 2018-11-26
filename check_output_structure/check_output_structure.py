# TODO: Check for photos too

import argparse
import csv
import os

parser = argparse.ArgumentParser(description='Check RipStation output structure')
parser.add_argument('--src', required=True, help='Target directory')
args = parser.parse_args()


# Function
# Check audio ODs
def check_optical_discs(src_path, disc_type):

    if disc_type == 'audio CD':
        print('Checking audio CDs...')
        audio_cd_list = get_target(src_path, disc_type)
        audio_cd_success_list = get_success_target(audio_cd_list)

        for row in audio_cd_success_list:
            # Looking for missing ___
            # TBA

            # Looking for missing DIPs
            if row['made_DIP?'] == 'Y' and os.path.isfile(os.path.join(src_path, row['barcode'], row['barcode'] + '.wav')) is False:
                print('No DIP!', row['barcode'])

    if disc_type == 'video DVD':
        print('Checking video DVDs...')
        video_dvd_list = get_target(src_path, disc_type)
        video_dvd_success_list = get_success_target(video_dvd_list)

        for row in video_dvd_success_list:
            # Looking for missing ___
            if os.path.isfile(os.path.join(src_path, row['barcode'], row['barcode'] + '.iso')) is False:
                print('No ISO!', row['barcode'])

            # Looking for missing DIPs
            if row['made_DIP?'] == 'Y' and os.path.isfile(os.path.join(src_path, row['barcode'], row['barcode'] + '.mp4')) is False:
                print('No DIP!', row['barcode'])

    if disc_type == 'data OD':
        print('Checking for data ODs')
        data_od_list = get_target(src_path, disc_type)
        data_od_success_list = get_success_target(data_od_list)

        for row in data_od_success_list:
            # Looking for false audio-rip
            if os.path.isfile(os.path.join(src_path, row['barcode'], row['barcode'], 'track01.cda')) is True:
                print(row['barcode'], 'looks like an audio CD to me.')

            # Looking for false video-rip
            if os.path.isdir(os.path.join(src_path, row['barcode'], row['barcode'], 'VIDEO_TS')) is True:
                print(row['barcode'], 'looks like a video DVD to me.')


# Parsing targets from bhl_inventory.csv and returning them in a list
def get_target(src_path, disc_type):
    return_list = []
    with open(os.path.join(src_path, 'bhl_inventory.csv'), mode='r') as bhl_inventory_csv_file:
        csv_reader = csv.DictReader(bhl_inventory_csv_file)

        if disc_type == 'audio CD' or disc_type == 'video DVD':
            for row in csv_reader:
                if row['media_type'] == disc_type:
                    return_list.append(dict(row))

        if disc_type is 'data OD':
            for row in csv_reader:
                if row['media_type'][:4] == disc_type[:4]:
                    return_list.append(dict(row))

    print('Found', len(return_list), disc_type, 'barcodes in bhl_inventory.csv file.')

    return return_list


# Parsing successful transfers from a list and returning them in a list
def get_success_target(src_list):
    return_list = []
    for row in src_list:
        if row['pass_1_successful?'] == 'Y' or row['pass_2_successful?'] == 'Y':
            return_list.append(row)

    return return_list


# Script
check_optical_discs(args.src, 'audio CD')
print()
check_optical_discs(args.src, 'video DVD')
print()
check_optical_discs(args.src, 'data OD')
