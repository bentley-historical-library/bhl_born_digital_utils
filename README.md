# BHL Ripstation (AKA Jackie) Utilities
Scripts used for Ripstation transfers at the Bentley Historical Library

![RipStation (AKA Jackie)](https://lh6.googleusercontent.com/1xcmHUrp4zAYeWjZuXk0liNkbZZB7jKz0xFvkuDUHSq0ydCT9Ga3sbNIkhFCtdgWrjCsDowgDOyXaDuDs4ey8cTbckZlmipm7kmbd6nTDynFvO9hJSEq74HXgDqbPjckHsp_ivxW)

## Table of Contents
- [check_empty_folder file.py](https://github.com/bentley-historical-library/bhl_ripstation_utils#check_empty_folder_filepy): Check for empty sub-directories and files in a directory.
- [check_missing_folder.py](https://github.com/bentley-historical-library/bhl_ripstation_utils#check_missing_folderpy): Check for missing sub-directories by comparing directory and bhl_inventory.csv
- [check_output_structure.py](https://github.com/bentley-historical-library/bhl_ripstation_utils#check_folder_structurepy): Check for RipStation output structure.
- [check_os files.py](https://github.com/bentley-historical-library/bhl_ripstation_utils#check_os_filespy): Check and DELETE operating system files in a directory.
- [make_dips.py](https://github.com/bentley-historical-library/bhl_ripstation_utils#make_dipspy): Make DIPs from RipStation audio (.wav) and video (.iso) output.
- [unhide_folder.py](https://github.com/bentley-historical-library/bhl_ripstation_utils#unhide_folderpy): Unhide hidden sub-directories in a directory.

## check_empty_folder_file.py
Check for empty sub-directories and files in a directory.

Usage: check_empty_folder_file.py [-h] -i PATH

Arguments:

| Argument | Help |
| --- | --- |
| -h, --help | Show this help message and exit |
| -i PATH, --input | Input directory |

## check_missing_folder.py
Check for missing sub-directories by comparing directory and bhl_inventory.csv.

Usage: check_missing_folder.py [-h] -i PATH

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

Usage: check_output_structure.py [-v] [-h] -i PATH

Arguments:

| Argument | Help |
| --- | --- |
| -v, --validation_off | Turn off validating .wav and .mp4 files |
| -h, --help | Show this help message and exit |
| -i PATH, --input | Input directory |

## check_os_files.py
Check and DELETE operating system files, such as Thumbs.db, .DS_store, Desktop DB, Desktop DF, in a directory.

Usage: check_os_files.py [-b] [-e] [-f] [-h] -i PATH

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

Usage: make_dips.py [-h] -i INPUT -o OUTPUT

Arguments:

| Argument | Help |
| --- | --- |
| -h, --help | show this help message and exit |
| -i PATH, --input | Input directory |
| -o PATH, --output | Output directory |

## unhide_folder.py
Unhide hidden sub-directories in a directory.

Usage: unhide_folder.py [-h] -i PATH

Arguments:

| Argument | Help |
| --- | --- |
| -h, --help | Show this help message and exit |
| -i PATH, --input | Input directory |