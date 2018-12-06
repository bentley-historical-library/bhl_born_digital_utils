# BHL RipStation (AKA Jackie) Utilities
RipStation scripts used by the Bentley Historical Library

![RipStation (AKA Jackie)](https://lh6.googleusercontent.com/1xcmHUrp4zAYeWjZuXk0liNkbZZB7jKz0xFvkuDUHSq0ydCT9Ga3sbNIkhFCtdgWrjCsDowgDOyXaDuDs4ey8cTbckZlmipm7kmbd6nTDynFvO9hJSEq74HXgDqbPjckHsp_ivxW)

## Table of Contents
  * [check_empty_folder](https://github.com/bentley-historical-library/bhl_ripstation_utils#check_empty_folder): Check for empty sub-directories and files in a directory.
  * [check_missing_folder](https://github.com/bentley-historical-library/bhl_ripstation_utils#check_missing_folder): Check for missing sub-directories by comparing directory and bhl_inventory.csv
  * [check_output_structure](https://github.com/bentley-historical-library/bhl_ripstation_utils#check_folder_structure): Check for RipStation output structure.
  * [check_thumbs_db_ds_store](https://github.com/bentley-historical-library/bhl_ripstation_utils#check_thumbs_db_ds_store): Check and DELETE Thumbs.DB and .DS_Store files in a directory.
  * [make_dips](https://github.com/bentley-historical-library/bhl_ripstation_utils#make_dips): Make DIPs from RipStation audio (.wav) and video (.iso) output.

---

## check_empty_folder
Check for empty sub-directories and files in a directory.

Usage: check_empty_folder.py [-h] --src SRC

Arguments:

| Argument | Help |
| --- | --- |
| --src SRC | Target directory |
| -h, --help | Show this help message and exit |

## check_missing_folder
Check for missing sub-directories by comparing directory and bhl_inventory.csv.

Usage: check_missing_folder.py [-h] --src SRC

Arguments:

| Argument | Help |
| --- | --- |
| --src SRC | Target directory |
| -h, --help | Show this help message and exit |

## check_output_structure
Check for RipStation output structure.

Usage: check_output_structure.py [-h] --src SRC

Arguments:

| Argument | Help |
| --- | --- |
| --src SRC | Target directory |
| -h, --help | Show this help message and exit |

## check_thumbs_db_ds_store
Check and DELETE Thumbs.DB and/or .DS_Store files in a directory.

Usage: check_thumbs_db_ds_store.py [-t_off] [d_off] [-h] --src SRC

Arguments:

| Argument | Help |
| --- | --- |
| --src SRC | Target directory |
| -t_off | Turn off deleting Thumbs.db files |
| -d_off | Turn off deleting .DS_Store files |
| -h, --help | Show this help message and exit |

## make_dips
Make dissemination information packages (DIPs) from RipStation audio (.wav) and video (.iso) output. 

Dependency:
This script uses FFmpeg and Handbreak CLI to create DIPs. 

- Download zipped [FFmpeg](https://www.ffmpeg.org/download.html) and [Handbreak CLI](https://handbrake.fr/downloads2.php) packages.
- Rename package folders to 'ffmepg' and 'HandBreakCLI'
- Place package folders in the same folder with make_dips.py.

Usage: make_dips.py [-h] --src SRC --dst DST

Arguments:

| Argument | Help |
| --- | --- |
| --src SRC | Input directory |
| --dst DST | Output directory |
| -h, --help | show this help message and exit |
