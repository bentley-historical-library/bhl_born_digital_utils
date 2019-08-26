import csv
import os
import subprocess

# Reference
# https://stackoverflow.com/questions/33344413/why-is-my-for-loop-skipping-an-element-in-my-list

# Reference for validate_using_ffmpeg()
# https://superuser.com/questions/100288/how-can-i-check-the-integrity-of-a-video-file-avi-mpeg-mp4
# https://stackoverflow.com/questions/4117530/sys-argv1-meaning-in-script
# http://openpreservation.org/blog/2017/01/04/breaking-waves-and-some-flacs/


def check_output_structure(src_path, validation_off):
    target_lists = get_targets(src_path)
    for media_type in target_lists.keys():
        check_structure(src_path, validation_off, target_lists[media_type], media_type)


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
                    target_lists[media_type] = {}
                target_lists[media_type].append(row)
    return target_lists


def check_structure(src_path, validation_off, target_list, media_type):
    for row in target_list:
        barcode = row.get("barcode").strip()
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
                    validate_using_ffmpeg(wav)

        elif media_type == "video":
            iso_path = os.path.join(target_path, "{}.iso".format(barcode))
            if not os.path.exists(iso_path):
                print("No .iso files found for {}".format(barcode))
            dip_exists = confirm_dip(row, target_path, barcode, "mp4")
            if dip_exists and not validation_off:
                dip_filepath = os.path.join(target_path, "{}.mp4".format(barcode))
                validate_using_ffmpeg(dip_filepath)

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
    if row.get("made_dip").lower().strip() in ["y", "yes"]:
        dip_filepath = os.path.join(target_path, "{}.{}".format(barcode, extension))
        if not os.path.exists(dip_filepath):
            print("No DIP file found for {}".format(barcode))
            return False
        else:
            return True
    else:
        return False


def validate_using_ffmpeg(media_path):
    ffmpeg_path = get_ffmpeg_path()
    print("Validating {}".format(media_path))
    cmd = [
        ffmpeg_path,
        "-loglevel", "error",
        "-i", media_path,
        "-f", "null", "-",
        "2>&1"
    ]
    p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    output = p.stdout.read().decode("ISO-8859-1")
    if not output:
        print("{} passed ffmped validation.".format(media_path))
    else:
        print("{} failed ffmped validation. See below for details:".format(media_path))
        print(output)


def get_ffmpeg_path():
    # update this to read from a config, take an argument, check if ffmpeg exists on path, etc.
    return r"C:\BHL\Utilities\ffmpeg\bin\ffmpeg.exe"
