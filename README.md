# BHL Born-digital Utilities
Scripts and templates used for born-digital transfers at the Bentley Historical Library

## Table of Contents
- [bhl_inventory.csv](https://github.com/bentley-historical-library/bhl_born_digital_utils#bhl_inventorycsv)
- [check_empty_folder file.py](https://github.com/bentley-historical-library/bhl_born_digital_utils#check_empty_folder_filepy): Check for empty sub-directories and files in a directory.
- [check_missing_folder.py](https://github.com/bentley-historical-library/bhl_born_digital_utils#check_missing_folderpy): Check for missing sub-directories by comparing directory and bhl_inventory.csv
- [check_output_structure.py](https://github.com/bentley-historical-library/bhl_born_digital_utils#check_folder_structurepy): Check for RipStation output structure.
- [check_os files.py](https://github.com/bentley-historical-library/bhl_born_digital_utils#check_os_filespy): Check and delete operating system files in a directory.
- [make_dips.py](https://github.com/bentley-historical-library/bhl_born_digital_utils#make_dipspy): Make DIPs from RipStation audio (.wav) and video (.iso) output.
- [rmw_transfer.py](https://github.com/bentley-historical-library/bhl_born_digital_utils#rmw_transferpy): Create a barcode directory, including bhl_metadata folder and bhl_notice file, in a accession directory.
- [robocopy.py](https://github.com/bentley-historical-library/bhl_born_digital_utils#robocopypy): Used to copy newly transferred content to the digital archive.
- [unhide_folder.py](https://github.com/bentley-historical-library/bhl_born_digital_utils#unhide_folderpy): Unhide hidden sub-directories in a directory.

## bhl_inventory.csv
A tracking template used for born-digital transfers at the Bentley Historical Library. See [README for bhl_inventory.csv](bhl_inventory/README.md).

## check_empty_folder_file.py
Check for empty sub-directories and files in a directory.

Usage: `check_empty_folder_file.py [-h] -i PATH`

Arguments:

| Argument | Help |
| --- | --- |
| -h, --help | Show this help message and exit |
| -i PATH, --input | Input directory |

## check_missing_folder.py
Check for missing sub-directories by comparing directory and bhl_inventory.csv.

Usage: `check_missing_folder.py [-h] -i PATH`

Arguments:

| Argument | Help |
| --- | --- |
| -h, --help | Show this help message and exit |
| -i PATH, --input | Input directory |

## check_output_structure.py
Check for RipStation output structure.

Dependency:
This script uses FFmpeg's -f null method to validate .wav and .mp4 files. 

- Download zipped [FFmpeg](https://www.ffmpeg.org/download.html) package.
- Rename package folders to 'ffmepg'.
- Place package folders in the same folder with check_output_structure.py.

Usage:
- On the command line, navigate (`cd`) to the directory that contains `check_output_structure.py`
- `check_output_structure.py [-v] [-h] -i PATH`

Arguments:

| Argument | Help |
| --- | --- |
| -v, --validation_off | Turn off validating .wav and .mp4 files |
| -h, --help | Show this help message and exit |
| -i PATH, --input | Input directory |

## check_os_files.py
Check and DELETE operating system files, such as Thumbs.db, .DS_store, Desktop DB, Desktop DF, in a directory.

Usage: `check_os_files.py [-b] [-e] [-f] [-h] -i PATH`

Arguments:

| Argument | Help |
| --- | --- |
| -b, --thumbsdb_off | Turn off deleting Thumbs.db files |
| -e, --dsstore_off | Turn off deleting .DS_Store files |
| -f, --desktopdbdf_off | Turn off deleting Desktop DB and Desktop DF files |
| -h, --help | Show this help message and exit |
| -i PATH, --input | Input directory |

## make_dips.py
Make dissemination information packages (DIPs) from RipStation audio (.wav) and video (.iso) output. 

Dependency:
This script uses FFmpeg and Handbreak CLI to create DIPs. 

- Download zipped [FFmpeg](https://www.ffmpeg.org/download.html) and [Handbreak CLI](https://handbrake.fr/downloads2.php) packages.
- Rename package folders to 'ffmepg' and 'HandBreakCLI'.
- Place package folders in the same folder with make_dips.py.

Usage:
- On the command line, navigate (`cd`) to the directory that contains `make_dips.py`
- `make_dips.py [-h] -i INPUT -o OUTPUT`

Arguments:

| Argument | Help |
| --- | --- |
| -h, --help | show this help message and exit |
| -i PATH, --input | Input directory |
| -o PATH, --output | Output directory |

## rmw_transfer.py
Create a barcode directory, including bhl_metadata folder and bhl_notice file, in a accession directory.

Dependency: 
- This script uses the Logitech Webcam's default file save location for getting images. 
- This script uses [Pillow](https://github.com/python-pillow/Pillow) to adjust images of removable media. 
- bhl_notice uses [JsBarcode](https://github.com/lindell/JsBarcode) CDN to a render Codabar barcode in the HTML document.  

Usage: `rmw_transfer.py [-m] [-n] --rmw NUMBER [-h] -i PATH`

Arguments:

| Argument | Help |
| --- | --- |
| -m, --metadata_off | Turn off creating bhl_metadata directory |
| -n, --notice_off | Turn off creating bhl_notice file |
| --rmw | RMW (Removable Media Workstation) Number (e.g., 1 or 2) |
| -h, --help | Show this help message and exit |
| -i PATH, --input | Input directory |

Acknowledgments:
- rmw_transfer.py is developed based on CollectionSetup.exe by [Matt Adair](mailto:mladair@umich.edu).

## robocopy.py
This is used to copy subdirectories listed in a folder using Windows 7 "robocopy" from the command line. A new folder must be created in the output directory prior to running this script. The log will be a text file located inside of the newly created folder.

Usage: `robocopy.py [-h] -i INPUT -o OUTPUT`

Arguments:

| Argument | Help |
| --- | --- |
| -h, --help | Show this help message and exit |
| -i PATH, --input | Input directory |
| -o PATH, --output | Output directory |

## unhide_folder.py
Unhide hidden sub-directories in a directory.

Usage: `unhide_folder.py [-h] -i PATH`

Arguments:

| Argument | Help |
| --- | --- |
| -h, --help | Show this help message and exit |
| -i PATH, --input | Input directory |
