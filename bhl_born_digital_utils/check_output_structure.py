import csv
import os
import subprocess
import re

from bhl_born_digital_utils.config import get_config_setting

# Reference
# https://stackoverflow.com/questions/33344413/why-is-my-for-loop-skipping-an-element-in-my-list
# https://docs.python.org/3.3/howto/regex.html#performing-matches
# https://stackoverflow.com/questions/1800817/how-can-i-get-part-of-regex-match-as-a-variable-in-python

# Reference for validate_using_ffmpeg()
# https://superuser.com/questions/100288/how-can-i-check-the-integrity-of-a-video-file-avi-mpeg-mp4
# https://stackoverflow.com/questions/4117530/sys-argv1-meaning-in-script
# http://openpreservation.org/blog/2017/01/04/breaking-waves-and-some-flacs/


def check_output_structure(src_path, validation_off, logs_dir):
    target_lists = get_targets(src_path)
    for media_type in target_lists.keys():
        check_structure(src_path, validation_off, target_lists[media_type], media_type, logs_dir)


def get_targets(src_path):
    target_lists = {}
    bhl_inventory = os.path.join(src_path, "bhl_inventory.csv")
    with open(bhl_inventory, "r", newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            media_type = row.get("media_type", "").lower().strip()
            if media_type.startswith("audio"):
                media_type = "audio"
            elif media_type.startswith("video"):
                media_type = "video"
            else:
                media_type = "data"
            pass_1 = row.get("pass_1_successful").lower().strip()
            pass_2 = row.get("pass_2_successful").lower().strip()
            separation = row.get("separation").lower().strip()
            if (pass_1 in ["y", "yes"] or pass_2 in ["y", "yes"]) and separation not in ["y", "yes"]:
                if media_type not in target_lists:
                    target_lists[media_type] = []
                target_lists[media_type].append(row)
    return target_lists


def check_structure(src_path, validation_off, target_list, media_type, logs_dir):
    for row in target_list:
        accession_number = os.path.split(src_path)[-1]
        barcode = row.get("barcode").strip()
        pattern = re.compile(barcode) # Setting pattern to search for later
        target_path = os.path.join(src_path, barcode)

        if media_type == "audio":
            wavs = []
            for root, dirnames, filenames in os.walk(target_path):
                for filename in filenames:
                    if filename.lower().endswith(".wav"):
                        wavs.append(os.path.join(target_path, filename))
            if len(wavs) == 0:
                print("No .wav files found for {}".format(barcode))
            dip_exists = confirm_dip(row, target_path, barcode, "wav")
            if not validation_off and len(wavs) > 0:
                for wav in wavs:
                    validate_using_ffmpeg(wav, accession_number, logs_dir)

        elif media_type == "video":
            new_mp4s = []
            mp4s = []
            new_isos = []
            isos = []
            for root, dirnames, filenames in os.walk(target_path):
                for filename in filenames:
                    if filename.lower().endswith(".mp4"): # find mp4s
                        barcode = filename.replace(".mp4", "")  # remove extension to make NEW barcode
                        new_mp4s.append(barcode)
                        if '-' in filename: # If there are multiple mp4 files
                            x = pattern.search(barcode) # Find the exact barcode match
                            if x: # If there is an exact match
                                y = x.group(0) # Create new var with exact match str
                                new_iso = os.path.join(target_path, y + ".iso") # Append .iso to trick program
                                new_isos.append(new_iso) # Add to temp list.
                        else: # If there is only 1 mp4 file
                            new_iso = filename.replace('.mp4', '.iso') # Replace extension
                            new_isos.append(os.path.join(target_path, new_iso)) # Add to temp list

                    for unique in new_isos: # Filter out duplicates
                        if unique not in isos:
                            isos.append(unique) # New list of unique mp4 file paths

                    for iso in isos: # Check for iso files
                        if not os.path.exists(iso): # Check exact file path matches
                            print("No .iso files found for {}".format(barcode))

            for barcode in new_mp4s: # Eliminate duplicate mp4s
                if barcode not in mp4s: # Then proceed to validation process
                    dip_exists = confirm_dip(row, target_path, barcode, "mp4")
                    if dip_exists and not validation_off:
                        dip_filepath = os.path.join(target_path, "{}.mp4".format(barcode))
                        validate_using_ffmpeg(dip_filepath, accession_number, logs_dir)

        else:
            audio_track = os.path.join(target_path, "track01.cda")
            if os.path.exists(audio_track):
                print("{} looks like an audio CD to me.".format(barcode))
            video_dir = os.path.join(target_path, "VIDEO_TS")
            if os.path.exists(video_dir):
                print("{} looks like a video DVD to me.".format(barcode))

        if row.get("took_photo").lower().strip() in ["y", "yes"]:
            media_0_filepath = os.path.join(target_path, "bhl_metadata", "media_0.jpg")
            if not os.path.exists(media_0_filepath):
                print("media_0.jpg not found in bhl_metadata for {}".format(barcode))


def confirm_dip(row, target_path, barcode, extension):
    dip_filepath = os.path.join(target_path, "{}.{}".format(barcode, extension))
    if row.get("made_dip").lower().strip() in ["y", "yes"] and not os.path.exists(dip_filepath):
        print("No DIP file found for {}".format(barcode))
        return False
    elif os.path.exists(dip_filepath):
        return True
    else:
        return False


def validate_using_ffmpeg(media_path, accession_number, logs_dir):
    ffmpeg_path = get_config_setting("ffmpeg", default="ffmpeg")
    log_path = get_log_path(media_path, accession_number, logs_dir)
    print("Validating {}".format(media_path))
    cmd = "{0} -loglevel error -i \"{1}\" -f null - 2>\"{2}\"".format(ffmpeg_path, media_path, log_path)
    subprocess.check_call(cmd, shell=True)
    if os.path.getsize(log_path) == 0:
        print("{} passed ffmpeg validation.".format(media_path))
    else:
        print("{} failed ffmpeg validation. See {} for details".format(media_path, log_path))


def get_log_path(media_path, accession_number, logs_dir):
    media_filename = os.path.split(media_path)[-1]
    if not os.path.exists(logs_dir):
        os.mkdir(logs_dir)
    accession_dir = os.path.join(logs_dir, accession_number)
    if not os.path.exists(accession_dir):
        os.mkdir(accession_dir)
    ffmpeg_dir = os.path.join(accession_dir, "ffmpeg")
    if not os.path.exists(ffmpeg_dir):
        os.mkdir(ffmpeg_dir)
    log_path = os.path.join(ffmpeg_dir, "{}.log".format(media_filename))
    return log_path
