import configparser
import os
import sys


def get_config_setting(setting, default=None):
    configuration = _load_config()
    try:
        result = configuration.get("defaults", setting)
        return result
    except (configparser.NoOptionError, configparser.NoSectionError):
        return default


def _load_config():
    config_file = os.path.join(os.path.expanduser("~"), ".bhl_bd_utils")
    config = configparser.ConfigParser()
    config.read(config_file)
    if not os.path.exists(config_file):
        print("bhl_born_digital_utils config file not found at {}".format(config_file))
        configure = input("would you like to create a configuration file? (y/n) ").strip()
        if configure.lower() in ["y", "yes"]:
            _create_config(config, config_file)
        else:
            print("Skipping create config")
    return config


def _create_config(config, config_file):
    print("The input directory is the local RMW directory where content is transferred to from removable media")
    print("This can be overrriden by passing an -i flag to any utility that uses the input directory")
    input_dir_input = input("Enter a default input directory: ")

    print("\n\n")
    print("The destination directory is the location where content will be copied to from the RMW")
    print("This can be overriden by passing a -d flag to any utility that uses the destination directory")
    destination_dir_input = input("Enter a default destination directory: ")

    print("\n\n")
    print("The output of various utilities (bulk_extractor, robocopy, rsync) will be stored in a logs directory")
    print("This can be overriden by passing a -l flag to any utility that uses the logs directory")
    logs_dir_input = input("Enter a default logs directory: ")

    print("\n\n")
    print("Separated removable media will be moved to a dedicated separations directory")
    print("This can be overriden by passing a --separations_dir flag to any utility that uses the separations directory")
    separations_dir_input = input("Enter a default separations directory: ")

    print("\n\n")
    print("The 'create removable media transfer' utility automatically renames and crops images of removable media from the default webcam directory")
    webcam_dir_input = input("Enter the directory where webcam images are saved: ")

    if "win" in sys.platform:
        print("\n\n")
        print("HandBrake CLI is used to create DIPs from the RipStation")
        handbrake_path_input = input("Enter the path to the HandBrakeCLI.exe for Windows machines: ")
        handbrake_path = _normalize_input(handbrake_path_input)

        print("\n\n")
        print("FFmpeg is used to create and validate access derivatives from the RipStation")
        ffmpeg_path_input = input("Enter the path to the FFmpeg.exe for Windows machines: ")
        ffmpeg_path = _normalize_input(ffmpeg_path_input)

        print("\n\n")
        print("bulk_extractor is used to scan for PII")
        be_path_input = input("Enter the path to the bulk_extractor.exe for Windows machines: ")
        be_path = _normalize_input(be_path_input)
    else:
        # assumes these are available on the system path for other OS's
        handbrake_path = "HandBrakeCLI"
        ffmpeg_path = "ffmpeg"
        be_path = "bulk_extractor"

    print("\n\n")
    print("The HandBrake CLI requires a preset file to generate derivatives")
    handbrake_preset_input = input("Enter the path to the HandBrake preset file: ")

    input_dir = _normalize_input(input_dir_input)
    logs_dir = _normalize_input(logs_dir_input)
    destination_dir = _normalize_input(destination_dir_input)
    separations_dir = _normalize_input(separations_dir_input)
    webcam_dir = _normalize_input(webcam_dir_input)
    handbrake_preset = _normalize_input(handbrake_preset_input)

    config.add_section("defaults")
    config.set("defaults", "input", input_dir)
    config.set("defaults", "logs", logs_dir)
    config.set("defaults", "destination", destination_dir)
    config.set("defaults", "separations", separations_dir)
    config.set("defaults", "webcam_dir", webcam_dir)
    config.set("defaults", "handbrake", handbrake_path)
    config.set("defaults", "handbrake_preset", handbrake_preset)
    config.set("defaults", "ffmpeg", ffmpeg_path)
    config.set("defaults", "bulk_extractor", be_path)
    _save_config(config, config_file)


def _normalize_input(input_dir):
    return os.path.normpath(input_dir.strip('"\' '))


def _save_config(config, config_file):
    with open(config_file, "w") as f:
        config.write(f)
