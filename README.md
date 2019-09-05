# BHL Born-digital Utilities
Scripts and templates used for born-digital transfers at the Bentley Historical Library

## Requirements

- Python 3: Required to run all utilities
- Pillow: To adjust images of removable media
- FFmpeg: To validate audio and video files
- bulk_extractor: To scan for PII
- rsync: To copy files on non-Windows machines

## bhl_inventory.csv
A tracking template used for born-digital transfers at the Bentley Historical Library. See [README for bhl_inventory.csv](bhl_inventory/README.md).

## bhl_born_digital_utils.py
This script serves as the entry point to various born-digital transfer utilities. A summary of the script's usage and available actions are below, followed by detailed instructions for each utility.

Usage: `bhl_born_digital_utils.py PATH action [options]`

| Action | Description |
| --- | --- |
| -c, --create_transfer | Create a RMW transfer |
| -e, --empty | Check for empty folders and files |
| -m, --missing | Check for missing barcodes and folders |
| -o, --osfiles | Check for and delete system files and directories |
| -s, --structure | Check RipStation output structure |
| -u, --unhide | Unhide folders (Windows workstations only) |
| -b, --bulkextractor | Run bulk_extractor |
| --copy | Copy accession from RMW |
| --move_separations | Move separations |
| --av_media | Separate AV media |

### Create a RMW transfer
Create barcode directories, bhl_metadata, and bhl_notices directories inside an accession directory

Requirements:
- This script uses the Logitech Webcam's default file save location for getting images. 
- This script uses [Pillow](https://github.com/python-pillow/Pillow) to adjust images of removable media. 
- bhl_notice uses [JsBarcode](https://github.com/lindell/JsBarcode) CDN to a render Codabar barcode in the HTML document.  

`bhl_born_digital_utils.py PATH -c/--create_transfer --rmw INT [--metadata_off] [--notices_off]`

| Argument | Help |
| --- | --- |
| PATH | Input directory (path to an accession directory) |
| -c, --create_transfer | Create a RMW transfer |
| --rmw | Removable media workstation number (either 1 or 2) |
| --metadata_off | Turn off creating bhl_metadata directory inside barcode folders |
| --notices_off | Turn off creating bhl_notices inside accession folder |

Acknowledgments: This utility is developed based on CollectionSetup.exe by [Matt Adair](mailto:mladair@umich.edu).

### Check for empty folders and files
Checks for empty directories and 0-byte files in a source directory and prints the results to the terminal

`bhl_born_digital_utils.py PATH -e/--empty`

| Argument | Help |
| --- | --- |
| PATH | Input directory |
| -e, --empty | Check for empty folders and files |

### Check for missing barcodes and folders
Parses the bhl_inventory.csv and subdirectories for a source directory, compares the results, and lists barcodes that are in the bhl_inventory.csv but not in the source directory and subdirectories in the source directory that are not accounted for in the bhl_inventory.csv

`bhl_born_digital_utils.py PATH -m/--missing`

| Argument | Help |
| --- | --- |
| PATH | Input directory|
| -m, --missing | Check for missing barcodes and folders |

### Check for and delete system files and directories
Checks for and deletes operating system files and directories in a source path. Operating system files checked include Thumbs.db, .DS_Store, Desktop DB, and Desktop DF. Operating system directories checked include .Trashes, .Spotlight-V100, and .fseventsd. The script will print all found files and directories to the terminal to confirm deletion. Optional arguments can turn off deleting Thumbs.db, .DS_Store, Desktop DB/DF, and directories (.Trashes, .Spotlight-V100, and .fseventsd).

`bhl_born_digital_utils.py PATH -o/--osfiles [--thumbsdb_off] [--dsstore_off] [--desktopdbdf_off] [--dirs_off]`

| Argument | Help |
| --- | --- |
| PATH | Input directory |
| -o, --osfiles | Check for and delete system files |
| --thumbsdb_off | Turn off deleting Thumbs.db files |
| --dsstore_off | Turn off deleting .DS_Store files |
| --desktopdbdf_off | Turn off deleting Desktop DB and Desktop DF files |
| --dirs_off | Turn off deleting .Trashes, .Spotlight-V100, and .fseventsd folders |

### Check RipStation output structure
Checks RipStation output structure, including checking to ensure that .mp4 and .wav DIPs have been made for video DVDs and audio CDs, respectively, that photos of removable media exist when applicable, and that .wav and .mp4 files are valid. Optional arguments can turn off validating .wav and .mp4 files.

Requirements: This script uses ffmpeg to validate .wav and .mp4 files. It currently expects ffmpeg to be installed in a very specific directory on the RMW workstation.

`bhl_born_digital_utils.py PATH -s/--structure [--validation_off]`

| Argument | Help |
| --- | --- |
| PATH | Input directory |
| --validation_off | Turn off validating .wav (audio CDs) and .mp4 (video DVDs) |

### Unhide folders
Unhide hidden sub-directories in a directory. Note: This removes the Windows -H (hidden) and -S (system) attributes from directories, and as such is only applicable on Windows machines.

`bhl_born_digital_utils.py PATH -u/--unhide`

| Argument | Help |
| --- | --- |
| PATH | Input directory |
| -u, --unhide | Unhide folders |

### Run bulk_extractor
This script will run the bulk_extractor.exe from the command line. Currently, scanning for exif metadata generated from images is turned off, and bulk_extractor will use its `accts` scanner to search for PII such as Social Security numbers, credit card numbers, telephone numbers, and email addresses. Reports generated by bulk_extractor will be stored in a logs subdirectory within the bhl_born_digital_utils root directory. In order to save time, resources, and to avoid false positives, bulk_extractor is not run on audio CDs or video DVDs. bulk_extractor reports are stored in subdirectories for each piece of removable media scanned. Following scanning, all empty reports are deleted, leaving only reports that had one or more hit.

Requirements: This utility requires that bulk_extractor is installed. It currently checks for the Windows version of bulk_extractor in a specific directory on the RMW workstation, and will attempt to use bulk_extractor on the system path in other environments.

`bhl_born_digital_utils.py PATH -b/--bulkextractor`

| Argument | Help |
| --- | --- |
| PATH | Input directory |
| -b, --bulkextractor | Run bulk_extractor |

### Copy accession from RMW
This utility copies a directory using robocopy (on Windows) or rsync. It takes an input directory and an output directory, and its primary purpose is to copy accessions from a removable media workstation to a network storage location. This utility will create a log file of the form `[accession_number]_[timestamp].txt` in a logs subdirectory in the bhl_born_digital_utils root directory.

`bhl_born_digital_utils.py PATH --copy -d/--destination PATH`

| Argument | Help |
| --- | --- |
| PATH | Input directory |
| -d, --destination | Destination directory |
| --copy | Copy accession from RMW |

### Move separations
This utility moves separated directories to a given destination directory. The script parses the bhl_inventory.csv in a given source directory to identify media that has been marked as separated by a `separation` column with a value of `y`, and then moves the `_barcode` directory from within the source directory to an `[accession]_separations` directory in the given destination. The script attempts to determine the accession number of a transfer by using the directory name of the source directory (e.g., `/path/to/source/1234` has an accesison number of `1234`). An accession number can be explicitly supplied with an optional `-a/--accession` argument.

`bhl_born_digital_utils.py PATH -d/--destination PATH [-a/--accession] ACCESSION --move_separations`

| Argument | Help |
| --- | --- |
| PATH | Input directory |
| -d, --destination | Destination directory |
| --move_separations | Move separations |
| -a, --accession | Accession number |

### Separate AV media
This utility moves audio-formatted CDs and video-formatted DVDs into their own directory so that AV content can be processed using Archivematica's automation-tools and data content can be sent to Archivematica's backlog. The script parses the bhl_inventory.csv in a given source directory to identify media with a `media_type` that begins with `audio` or `video` and then moves those barcode directories into a new directory named `[accession]_audiovisual` in the source directory's parent directory. For example, given a source directory of `/path/to/source/1234`, the script will move audiovisual media into `/path/to/source/1234_audiovisual`. The script attempts to determine the accession number of a transfer by using the directory name of the source directory. An accession number can be explicitly supplied with an optional `-a/--accession` argument.

| Argument | Help |
| --- | --- |
| PATH | Input directory |
| --av_media | Separate AV media |
| -a, --accession | Accession number |

## make_dips.py
Warning: This script has not yet been integrated in bhl_born_digital_utils.py

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
