import csv
import os
import re
import shutil
import subprocess

from bhl_born_digital_utils.config import get_config_setting


# Function
def get_target(src_path):
    return_list = []
    bhl_inventory = os.path.join(src_path, "bhl_inventory.csv")
    with open(bhl_inventory, mode='r') as bhl_inventory_csv_file:
        csv_reader = csv.DictReader(bhl_inventory_csv_file)
        csv_reader.fieldnames = [fieldname.strip().lower() for fieldname in csv_reader.fieldnames]

        # Removing non-targets, rows that are not audio CD or video DVD
        for row in csv_reader:
            barcode = row["barcode"]
            if row.get("separation", "").lower() in ["y", "yes"]:
                continue
            if row.get("pass_1_successful", "").lower() in ["n", "no"] and row.get("pass_2_successful", "").lower() in ["n", "no"]:
                continue

            if row['media_type'] in ["audio CD", "video DVD"]:
                barcode_and_media_type = [barcode, row["media_type"]]
                if row["media_type"] == "audio CD":
                    existing_dip = os.path.join(src_path, "{}.wav".format(barcode))
                    if not os.path.exists(existing_dip):
                        return_list.append(barcode_and_media_type)
                elif row["media_type"] == "video DVD":
                    existing_dip = [filename for filename in os.listdir(src_path) if filename.endswith(".mp4")]
                    if len(existing_dip) == 0:
                        return_list.append(barcode_and_media_type)
        return return_list


# Forked from Max's script
def mk_wav(src, barcode):
    print('Making .WAV for barcode ' + barcode)
    item_dir = os.path.join(src, barcode)
    out_filepath = os.path.join(item_dir, "{}.wav".format(barcode))
    ffmpeg_path = get_config_setting("ffmpeg", default="ffmpeg")

    # writing temporary input text file
    tracks = [name for name in os.listdir(item_dir) if name.endswith('.wav')]
    tmp_list = os.path.join(item_dir, "mylist.txt")
    with open(tmp_list, mode='w') as f:
        for track in sorted(tracks):
            track_path = os.path.join(item_dir, track)
            f.write("file '" + track_path + "'\n")

    # concatenating
    cmd = [
        ffmpeg_path,
        '-f', 'concat',
        '-safe', '0',
        '-i', tmp_list,
        '-c', 'copy',
        out_filepath
    ]
    exit_code = subprocess.call(cmd)

    # deleting temporary input text file
    os.remove(tmp_list)
    result = [barcode, exit_code]
    return result


# Forked from Max's script
def mk_mp4(src, barcode):
    handbrake_path = get_config_setting("handbrake", default="HandBrakeCLI")
    handbrake_preset = get_config_setting("handbrake_preset")
    results = []
    item_dir = os.path.join(src, barcode)
    isos = [filename for filename in os.listdir(item_dir) if filename.split(".")[-1].startswith("iso")]
    tmp_iso = os.path.join(item_dir, "tmp_{}.iso".format(barcode))
    # merge multiple isos to pass to HandBrake
    if len(isos) > 1:
        with open(tmp_iso, "wb") as f_out:
            for iso in isos:
                iso_path = os.path.join(item_dir, iso)
                with open(iso_path, "rb") as f_in:
                    shutil.copyfileobj(f_in, f_out)
        iso_path = tmp_iso
        # and then delete the concatenated iso when you're done
    elif len(isos) == 1:
        iso_path = os.path.join(item_dir, isos[0])

    # get title count
    cmd = [
        handbrake_path,
        '-i', iso_path,
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

    # make mp4 for single-title DVD
    if title_count == 1:
        print('\nMaking .MP4 for ' + barcode)
        out_filepath = os.path.join(item_dir, "{}.mp4".format(barcode))
        cmd = [
            handbrake_path,
            "--preset-import-file", handbrake_preset,
            "-i", iso_path,
            "-o", out_filepath
        ]

        exit_code = subprocess.call(cmd)
        result = [barcode, exit_code]
        results.append(result)

    # make mp4 for each title in multi-title DVD
    else:
        count = 1
        while count <= title_count:
            print('\nMaking .MP4 for title ' + str(count) + ' of ' + str(title_count))
            out_filepath = os.path.join(item_dir, "{}-{}.mp4".format(barcode, count))

            cmd = [
                handbrake_path,
                '--title', str(count),
                "--preset-import-file", handbrake_preset,
                '-i', iso_path,
                '-o', out_filepath
            ]

            exit_code = subprocess.call(cmd)
            result = ["barcode-{}".format(count), exit_code]
            results.append(result)
            count += 1
    if os.path.exists(tmp_iso):
        os.remove(tmp_iso)
    return results


def make_dips(src):
    # Script
    target_list = get_target(src)
    result_list = []

    for target in target_list:
        if target[1] == 'audio CD':
            result = mk_wav(src, target[0])
            result_list.append(result)

        if target[1] == 'video DVD':
            results = mk_mp4(src, target[0])
            result_list.extend(results)

    for result in result_list:
        if result[1] == 0:
            print(result[0], 'success with exit code', + result[1])

        else:
            print(result[0], 'fail with exit code', + result[1])
