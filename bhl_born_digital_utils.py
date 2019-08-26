import argparse
import sys

from bhl_born_digital_utils.rmw_transfer import create_rmw_transfer
from bhl_born_digital_utils.check_empty_folder_file import check_empty_folder_file
from bhl_born_digital_utils.check_missing_folder import check_missing_folder
from bhl_born_digital_utils.check_os_files import check_os_files
from bhl_born_digital_utils.check_output_structure import check_output_structure
from bhl_born_digital_utils.unhide_folders import unhide_folders
from bhl_born_digital_utils.copy_accession import copy_accession
from bhl_born_digital_utils.runbe import run_bulk_extractor


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("input", help="Input directory")

    parser.add_argument("-c", "--create_transfer", action="store_true", help="Create a RMW transfer")
    parser.add_argument("--rmw", type=int, choices=range(1, 3), help="Removable Media Workstation (RMW) number")
    parser.add_argument("--metadata_off", action="store_true", help="Turn off creating bhl_metadata")
    parser.add_argument("--notices_off", action="store_true", help="Turn off creating bhl_notices")

    parser.add_argument("-e", "--empty", action="store_true", help="Check for empty folders and files")

    parser.add_argument("-m", "--missing", action="store_true", help="Check for missing barcodes and folders")

    parser.add_argument("-o", "--osfiles", action="store_true", help="Check for and delete system files")
    parser.add_argument("--thumbsdb_off", action="store_true", default=False, help="Turn off deleting Thumbs.db files")
    parser.add_argument("--dsstore_off", action="store_true", default=False, help="Turn off deleting .DS_Store files")
    parser.add_argument("--desktopdbdf_off", action="store_true", default=False, help="Turn off deleting Desktop DB and Desktop DF files")
    parser.add_argument("--dirs_off", action="store_true", default=False, help="Turn off deleting .Trashes, .Spotlight-V100, and .fseventsd folders")

    parser.add_argument("-s", "--structure", action="store_true", help="Check RipStation output structure")
    parser.add_argument("--validation_off", action="store_true", help="Turn off validating audio CDs and video DVDs")

    parser.add_argument("-u", "--unhide", action="store_true", help="Unhide folders")

    parser.add_argument("--copy", action="store_true", help="Copy accession from RMW")
    parser.add_argument("-d", "--destination", help="Destination directory")

    parser.add_argument("-b", "--bulkextractor", action="store_true", help="Run bulk_extractor")

    args = parser.parse_args()

    if args.create_transfer:
        if not args.rmw:
            print("Please pass a Removable Media Workstation number [--rmw]")
            sys.exit()
        create_rmw_transfer(args.input, args.rmw, args.metadata_off, args.notices_off)
    if args.empty:
        check_empty_folder_file(args.input)
    if args.missing:
        check_missing_folder(args.input)
    if args.osfiles:
        check_os_files(args.input, args.thumbsdb_off, args.dsstore_off, args.desktopdbdf_off, args.dirs_off)
    if args.structure:
        check_output_structure(args.input, args.validation_off)
    if args.unhide:
        unhide_folders(args.input)
    if args.copy:
        if not args.destination:
            print("Please pass a path to destination directory [-d]")
            sys.exit()
        copy_accession(args.input, args.destination)
    if args.bulkextractor:
        run_bulk_extractor(args.input)


if __name__ == "__main__":
    main()
