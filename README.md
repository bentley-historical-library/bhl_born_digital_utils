# BHL Born-digital Utilities
Scripts and templates used for born-digital transfers at the Bentley Historical Library

## Table of Contents
- [bhl_inventory.csv](https://github.com/bentley-historical-library/bhl_born_digital_utils#bhl_inventorycsv)
- [check_empty_folder file.py](https://github.com/bentley-historical-library/bhl_born_digital_utils#check_empty_folder_filepy): Check for empty sub-directories and files in a directory.
- [check_missing_folder.py](https://github.com/bentley-historical-library/bhl_born_digital_utils#check_missing_folderpy): Check for missing sub-directories by comparing directory and bhl_inventory.csv
- [check_output_structure.py](https://github.com/bentley-historical-library/bhl_born_digital_utils#check_folder_structurepy): Check for RipStation output structure.
- [check_os files.py](https://github.com/bentley-historical-library/bhl_born_digital_utils#check_os_filespy): Check and delete operating system files in a directory.
- [make_dips.py](https://github.com/bentley-historical-library/bhl_born_digital_utils#make_dipspy): Make DIPs from RipStation audio (.wav) and video (.iso) output.
- [optical_types.py](https://github.com/bentley-historical-library/bhl_born_digital_utilss#optical_typespy): Sort optical disc types listed in a csv inventory and robocopy content from filtered optical discs.
- [rmw_transfer.py](https://github.com/bentley-historical-library/bhl_born_digital_utils#rmw_transferpy): Create a barcode directory, including bhl_metadata folder and bhl_notice file, in a accession directory.
- [robocopy.py](https://github.com/bentley-historical-library/bhl_born_digital_utils#robocopypy): Used to copy newly transferred content to the digital archive.
- [runbe.py](https://github.com/bentley-historical-library/bhl_born_digital_utils#runbepy): Run bulk extractor from the command line.
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

## optical_types.py
This is used to filter inventoried barcodes by the optical disc type listed in a CSV file inventory and robocopy selected folders and corresponding content to a temporary folder. Specifically, inventoried barcodes with optical disc types listed as 'audio CD' or 'video DVD' will not be robocopied to a new directory because Bulk Extractor does not accurately scan for PII with those files. In addition, inventoried barcodes marked for separation will not be robocopied. The purpose for utilizing robocopy is to successfully copy challenging file paths that various Python libraries can not handle. The call for robocopy follow the Windows 7 parameters and will need to be updated when computers are running on Windows 10.

Usage: `optical_types.py [-h] -i INPUT -o OUTPUT`

Arguments:

| Argument | Help |
| --- | --- |
| -h, --help | Show this help message and exit |
| -i PATH, --input | CSV file |
| -o PATH, --outpt | Scan content directory |


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

## runbe.py
This script will run the bulk_extractor.exe from the command line. Currently, scanning for exif metadata generated from images is turned off. See the manual in the bulk extractor folder for more parameters. To run the script, you must encapsulate the input path in double quotes in the command line or else the script will not run. 

Usage: `runbe.py [-h] -i "<input/folder/path>"`

Arguments:

| Argument | Help |
| --- | --- |
| -h, --help | Show this help message and exit |
| -i PATH, --input | Input directory |

## unhide_folder.py
Unhide hidden sub-directories in a directory.

Usage: `unhide_folder.py [-h] -i PATH`

Arguments:

| Argument | Help |
| --- | --- |
| -h, --help | Show this help message and exit |
| -i PATH, --input | Input directory |
