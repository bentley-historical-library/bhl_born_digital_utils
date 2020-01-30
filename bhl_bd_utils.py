#!/usr/bin/env python

import argparse
import os

from bhl_born_digital_utils.rmw_transfer import create_rmw_transfer
from bhl_born_digital_utils.check_empty_folder_file import check_empty_folder_file
from bhl_born_digital_utils.check_missing_folder import check_missing_folder
from bhl_born_digital_utils.check_os_files import check_os_files
from bhl_born_digital_utils.check_output_structure import check_output_structure
from bhl_born_digital_utils.config import get_config_setting
from bhl_born_digital_utils.unhide_folders import unhide_folders
from bhl_born_digital_utils.copy_accession import copy_accession
from bhl_born_digital_utils.runbe import run_bulk_extractor
from bhl_born_digital_utils.move_separations import move_separations
from bhl_born_digital_utils.separate_av_media import separate_av_media
from bhl_born_digital_utils.rename_files import rename_files
from bhl_born_digital_utils.make_dips import make_dips
from bhl_born_digital_utils.run_brunnhilde import run_brunnhilde


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("accession", help="Accession number")

    directory_args = parser.add_argument_group("directories")
    directory_args.add_argument("--base", choices=["local", "remote"], default="local", help="Base location for directories")
    directory_args.add_argument("-i", "--input", help="Input directory")
    directory_args.add_argument("-d", "--destination", help="Destination directory")
    directory_args.add_argument("-l", "--logs", help="Logs directory")
    directory_args.add_argument("--separations_dir", help="Separations directory")

    action_args = parser.add_argument_group("actions")
    action_args.add_argument("-c", "--create_transfer", action="store_true", help="Create a RMW transfer")
    action_args.add_argument("--metadata_off", action="store_true", help="Turn off creating bhl_metadata")
    action_args.add_argument("--notices_off", action="store_true", help="Turn off creating bhl_notices")

    action_args.add_argument("-e", "--empty", action="store_true", help="Check for empty folders and files")

    action_args.add_argument("-m", "--missing", action="store_true", help="Check for missing barcodes and folders")

    action_args.add_argument("-o", "--osfiles", action="store_true", help="Check for and delete system files")
    action_args.add_argument("--thumbsdb_off", action="store_true", default=False, help="Turn off deleting Thumbs.db files")
    action_args.add_argument("--dsstore_off", action="store_true", default=False, help="Turn off deleting .DS_Store files")
    action_args.add_argument("--desktopdbdf_off", action="store_true", default=False, help="Turn off deleting Desktop DB and Desktop DF files")
    action_args.add_argument("--dirs_off", action="store_true", default=False, help="Turn off deleting .Trashes, .Spotlight-V100, and .fseventsd folders")

    action_args.add_argument("-s", "--structure", action="store_true", help="Check RipStation output structure")
    action_args.add_argument("--validation_off", action="store_true", help="Turn off validating audio CDs and video DVDs")

    action_args.add_argument("-u", "--unhide", action="store_true", help="Unhide folders")

    action_args.add_argument("--copy", action="store_true", help="Copy accession from RMW")

    action_args.add_argument("-b", "--bulkextractor", action="store_true", help="Run bulk_extractor")

    action_args.add_argument("--move_separations", action="store_true", help="Move separations")

    action_args.add_argument("--av_media", action="store_true", help="Separate AV media")

    action_args.add_argument("--rename_files", action="store_true", help="Rename files with invalid characters")

    action_args.add_argument("--dips", action="store_true", help="Make DIPs")

    action_args.add_argument("--brunnhilde", action="store_true", help="Run Brunnhilde (Linux only)")

    args = parser.parse_args()

    if args.input:
        input_dir = args.input
    else:
        setting = "input"
        if args.base == "remote":
            setting = "destination"
        input_dir = get_config_setting(setting)

    accession_number = args.accession
    accession_dir = os.path.join(input_dir, accession_number)

    if args.create_transfer:
        create_rmw_transfer(accession_dir, args.metadata_off, args.notices_off)
    if args.empty:
        check_empty_folder_file(accession_dir)
    if args.missing:
        check_missing_folder(accession_dir)
    if args.osfiles:
        check_os_files(accession_dir, args.thumbsdb_off, args.dsstore_off, args.desktopdbdf_off, args.dirs_off)
    if args.structure:
        if args.logs:
            logs_dir = args.logs
        else:
            logs_dir = get_config_setting("logs")
        check_output_structure(accession_dir, args.validation_off, logs_dir)
    if args.unhide:
        unhide_folders(accession_dir)
    if args.move_separations:
        if args.separations_dir:
            separations_dir = args.separations_dir
        else:
            separations_dir = get_config_setting("separations")
        move_separations(accession_dir, separations_dir, accession_number)
    if args.av_media:
        separate_av_media(accession_dir, accession_number)
    if args.copy:
        if args.destination:
            destination_dir = args.destination
        else:
            destination_dir = get_config_setting("destination")

        if args.logs:
            logs_dir = args.logs
        else:
            logs_dir = get_config_setting("logs")
        copy_accession(accession_dir, destination_dir, logs_dir)
    if args.bulkextractor:
        if args.logs:
            logs_dir = args.logs_dir
        else:
            logs_dir = get_config_setting("logs")
        run_bulk_extractor(accession_dir, logs_dir)
    if args.rename_files:
        rename_files(accession_dir)
    if args.dips:
        make_dips(accession_dir)
    if args.brunnhilde:
        run_brunnhilde(accession_dir, accession_number)


if __name__ == "__main__":
    main()
