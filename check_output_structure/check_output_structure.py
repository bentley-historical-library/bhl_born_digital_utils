import argparse
import csv
import os
import subprocess

import time

parser = argparse.ArgumentParser(description='Check RipStation output structure')
parser.add_argument('-voff', '--validation_off', action="store_true", default=False,
                    help='Turn off validating audio CD and video DVD')
parser.add_argument('-src', required=True, help='Target directory')
args = parser.parse_args()

# Reference
# https://stackoverflow.com/questions/33344413/why-is-my-for-loop-skipping-an-element-in-my-list

# Reference for validate_using_ffmpeg()
# https://superuser.com/questions/100288/how-can-i-check-the-integrity-of-a-video-file-avi-mpeg-mp4
# https://stackoverflow.com/questions/4117530/sys-argv1-meaning-in-script
# http://openpreservation.org/blog/2017/01/04/breaking-waves-and-some-flacs/


# Function
def check_optical_discs(src_path, val_off, disc_type):

    if disc_type == 'audio CD':
        print('Checking audio CDs...')
        audio_cd_list = get_target(src_path, disc_type)
        audio_cd_success_list = get_success_target(audio_cd_list)

        for row in audio_cd_success_list:
            src_bar_path = os.path.join(src_path, row['barcode'])

            audio_file_count = 0
            audio_file_list = []
            for dirpath, dirs, files in os.walk(src_bar_path):
                for file in files:
                    if file.lower().endswith('.wav'):
                        audio_file_count += 1
                        audio_file_list.append(file)

            # Looking for missing SIPs
            if audio_file_count == 0:
                print('No .wav file(s) for ' + row['barcode'] + '.')

            audio_dip_exist = os.path.isfile(os.path.join(src_bar_path, row['barcode'] + '.wav'))

            # Looking for missing DIPs
            if row['made_DIP?'] == 'Y' and audio_dip_exist is False:
                print('No DIP file for ' + row['barcode'] + '.')

            # Validating SIPs and DIPs
            if val_off is False and audio_file_count > 0:
                for audio_file in audio_file_list:
                    audio_file_path = os.path.join(src_bar_path, audio_file)
                    validate_using_ffmpeg(audio_file, audio_file_path)

            # Looking for missing bhl_metadata
            media_0_exist = os.path.isfile(os.path.join(src_bar_path, 'bhl_metadata', 'media_0.jpg'))
            if row['took_photo?'] == 'Y' and media_0_exist is False:
                print('No bhl_metadata file(s) for ' + row['barcode'] + '.')

    if disc_type == 'video DVD':
        print('Checking video DVDs...')
        video_dvd_list = get_target(src_path, disc_type)
        video_dvd_success_list = get_success_target(video_dvd_list)

        for row in video_dvd_success_list:
            src_bar_path = os.path.join(src_path, row['barcode'])

            video_sip_exist = os.path.isfile(os.path.join(src_bar_path, row['barcode'] + '.iso'))

            # Looking for missing SIPs
            if video_sip_exist is False:
                print('No .iso file(s) for ' + row['barcode'] + '.')

            video_dip_exist = os.path.isfile(os.path.join(src_bar_path, row['barcode'] + '.mp4'))

            # Looking for missing DIPs
            if row['made_DIP?'] == 'Y' and video_dip_exist is False:
                print('No DIP file for ' + row['barcode'] + '.')

            # Validating DIPs
            if val_off is False and row['made_DIP?'] == 'Y' and video_dip_exist is True:
                video_dip = row['barcode'] + '.mp4'
                video_dip_path = os.path.join(src_bar_path, row['barcode'] + '.mp4')
                validate_using_ffmpeg(video_dip, video_dip_path)

            # Looking for missing bhl_metadata
            media_0_exist = os.path.isfile(os.path.join(src_bar_path, 'bhl_metadata', 'media_0.jpg'))
            if row['took_photo?'] == 'Y' and media_0_exist is False:
                print('No bhl_metadata file(s) for ' + row['barcode'] + '.')

    if disc_type == 'data OD':
        print('Checking for data ODs')
        data_od_list = get_target(src_path, disc_type)
        data_od_success_list = get_success_target(data_od_list)

        for row in data_od_success_list:
            src_bar_path = os.path.join(src_path, row['barcode'])

            # Looking for false audio-rip
            if os.path.isfile(os.path.join(src_bar_path, 'track01.cda')) is True:
                print(row['barcode'] + ' looks like an audio CD to me.')

            # Looking for false video-rip
            if os.path.isdir(os.path.join(src_bar_path, 'VIDEO_TS')) is True:
                print(row['barcode'] + ' looks like a video DVD to me.')

            # Looking for missing bhl_metadata
            media_0_exist = os.path.isfile(os.path.join(src_bar_path, 'bhl_metadata', 'media_0.jpg'))
            if row['took_photo?'] == 'Y' and media_0_exist is False:
                print('No bhl_metadata file(s) for ' + row['barcode'] + '.')


# Parsing targets from bhl_inventory.csv and returning them in a list
def get_target(src_path, disc_type):
    return_list = []
    with open(os.path.join(src_path, 'bhl_inventory.csv'), mode='r') as bhl_inventory_csv_file:
        csv_reader = csv.DictReader(bhl_inventory_csv_file)

        if disc_type == 'audio CD' or disc_type == 'video DVD':
            for row in csv_reader:
                if row['media_type'] == disc_type:
                    return_list.append(dict(row))

        if disc_type == 'data OD':
            for row in csv_reader:
                if row['media_type'][:4] == disc_type[:4]:
                    return_list.append(dict(row))

    print('Found', len(return_list), disc_type, 'barcodes in bhl_inventory.csv file.')

    return return_list


# Parsing successful transfers from a list and returning them in a list
def get_success_target(src_list):
    temp_list = []
    return_list = []

    for row in src_list:
        # For Jackie bhl_inventory
        if 'pass_1_successful?' in row:
            if row['pass_1_successful?'] == 'Y' or row['pass_2_successful?'] == 'Y':
                temp_list.append(row)

        # For RMW bhl_inventory
        if 'pass_successful?' in row:
            if row['pass_successful?'] == 'Y':
                temp_list.append(row)

    return_list = temp_list.copy()

    for row in temp_list:
        if row['separation?'] == 'Y':
            return_list.remove(row)

    return return_list


# Validating media files using ffmpeg -f null method
def validate_using_ffmpeg(media, media_path):
    # print('Validating ' + media)
    cmd = [
        os.path.join('ffmpeg', 'bin', 'ffmpeg.exe'),
        '-loglevel', 'error',   
        '-i', media_path,
        '-f', 'null', '-',
        '2>&1',  # https://stackoverflow.com/questions/818255/in-the-shell-what-does-21-mean
    ]

    p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    output = p.stdout.read().decode('ISO-8859-1')

    if not output:
        print(media, 'passed ffmpeg validation.')
    else:
        print(media, 'failed ffmpeg validation (See below for details):')
        print(output)


# Script
start_time = time.time()
check_optical_discs(args.src, args.validation_off, 'audio CD')
print()
check_optical_discs(args.src, args.validation_off, 'video DVD')
print()
check_optical_discs(args.src, args.validation_off, 'data OD')
print()
end_time = time.time()
print("--- %s seconds ---" % (end_time - start_time))
