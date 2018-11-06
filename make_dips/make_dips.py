import argparse
import csv
import os
import subprocess
import re

parser = argparse.ArgumentParser(description='Make A/V DIPs from the RipStation (AKA Jackie).')
parser.add_argument('--src', required=True, help='Input directory')
parser.add_argument('--dst', required=True, help='Output directory')
args = parser.parse_args()


# Function
def get_target(src_path, dst_path):
    tmp_list = []
    exp_list = []
    with open(os.path.join(src_path, 'bhl_inventory.csv'), mode='r') as inventory_csv_file:
        csv_reader = csv.DictReader(inventory_csv_file)

        # Removing non-targets, rows that are not audio CD or video DVD
        for row in csv_reader:
            if row['media_type'] == 'audio CD' or row['media_type'] == 'video DVD':
                tmp_list.append(dict(row))

        # Removing non-targets, rows that have DIP made using this script
        for row in tmp_list:
            if row['media_type'] == 'audio CD':
                if os.path.isfile(os.path.join(dst_path, row['barcode'] + '.wav')) == True:
                    tmp_list.remove(row)

            if row['media_type'] == 'video DVD':
                if os.path.isfile(os.path.join(dst_path, row['barcode'] + '.mp4')) == True:
                    tmp_list.remove(row)

        # Adding targets, rows that are successful and have no DIP made
        for row in tmp_list:
            if row['pass_1_successful?'] == 'Y' and row['made DIP?'] != 'Y':
                barcode_and_media_type = [row['barcode'], row['media_type']]
                exp_list.append(barcode_and_media_type)

            if row['pass_1_successful?'] == 'N' and row['pass_2_successful?'] == 'Y' and row['made DIP?'] != 'Y':
                barcode_and_media_type = [row['barcode'], row['media_type']]
                exp_list.append(barcode_and_media_type)

        return exp_list

# def validate_target:


# Forked from Max's script
def mk_wav(src, barcode, dst):
    print('Making .WAV for barcode ' + barcode)

    # writing temporary input text file
    tracks = [name for name in os.listdir(os.path.join(src, barcode)) if name.endswith('.wav')]
    with open(os.path.join(src, barcode, 'mylist.txt'), mode='w') as f:
        for track in sorted(tracks):
            f.write("file '" + os.path.join(src, barcode, track) + "'\n")

    # concatenating
    cmd = [
        os.path.join('ffmpeg', 'bin', 'ffmpeg.exe'),
        '-f', 'concat',
        '-safe', '0',
        '-i', os.path.join(src, barcode, 'mylist.txt'),
        '-c', 'copy',
        os.path.join(dst, barcode + '.wav')
    ]
    exit_code = subprocess.call(cmd)

    # deleting temporary input text file
    os.remove(os.path.join(src, barcode, 'mylist.txt'))

    return [barcode, exit_code]


# Forked from Max's script
def mk_mp4(src, barcode, dst):
    for name in os.listdir(os.path.join(src, barcode)):
        if os.path.splitext(name)[1].startswith('.iso'):

            # get title count
            cmd = [
                os.path.join('HandBrakeCLI', 'HandBrakeCLI.exe'),
                '-i', os.path.join(src, barcode, name),
                '-t', '0'
            ]
            # https://www.saltycrane.com/blog/2008/09/how-get-stdout-and-stderr-using-python-subprocess-module/
            p = subprocess.Popen(cmd, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                                 stderr=subprocess.STDOUT)
            output = p.stdout.read().decode('ISO-8859-1')  # utf-8
            match = re.findall('scan: DVD has (\d+) title\(s\)', output)

            title_count = 1

            if match:
                title_count = int(match[0])

            # make mp4 for barcode
            if title_count == 1:
                print('\nMaking .MP4 for ' + barcode)

                cmd = [
                    os.path.join('HandBrakeCLI', 'HandBrakeCLI.exe'),
                    '-Z', 'High Profile',
                    '-i', os.path.join(src, barcode, name),
                    '-o', os.path.join(dst, os.path.splitext(name)[0] + '.mp4')
                ]
                exit_code = subprocess.call(cmd)

                return [barcode, exit_code]

            # make mp4 for each title in barcode
            else:
                count = 1
                while count <= title_count:
                    print('\nMaking .MP4 for title ' + str(count) + ' of ' + str(title_count))

                    cmd = [
                        os.path.join('HandBrakeCLI', 'HandBrakeCLI.exe'),
                        '--title', str(count),
                        '-Z', 'High Profile',
                        '-i', os.path.join(src, barcode, name),
                        '-o', os.path.join(dst, os.path.splitext(name)[0] + '-' + str(count) + '.mp4')
                    ]
                    exit_code = subprocess.call(cmd)

                    count += 1

                    return [barcode, exit_code]


# Script
target_list = get_target(args.src, args.dst)
print (target_list)
result_list = []

for target in target_list:
    if target[1] == 'audio CD':
        result = mk_wav(args.src, target[0], args.dst)
        result_list.append(result)

    if target[1] == 'video DVD':
        result = mk_mp4(args.src, target[0], args.dst)
        result_list.append(result)

for result in result_list:
    if result[1] == 0:
        print(result[0], 'success with exit code', + result[1])

    else:
        print(result[0], 'fail with exit code', + result[1])