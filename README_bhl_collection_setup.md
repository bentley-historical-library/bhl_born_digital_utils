# BHL Collection Setup
Scripts used to initiate removable media transfers at the Bentley Historical Library

## rmw_transfer.py
Create a barcode directory, including bhl_metadata folder and bhl_notice file, in a accession directory.

Dependency: 
- This script uses the Logitech Webcam's default file save location for getting images. 
- This script uses [Pillow](https://github.com/python-pillow/Pillow) to adjust images of removable media. 
- bhl_notice uses [JsBarcode](https://github.com/lindell/JsBarcode) CDN to a render Codabar barcode in the HTML document.  

Usage: rmw_transfer.py [-m] [-n] --rmw NUMBER [-h] -i PATH

Arguments:

| Argument | Help |
| --- | --- |
| -m, --metadata_off | Turn off creating bhl_metadata directory |
| -n, --notice_off | Turn off creating bhl_notice file |
| --rmw | RMW (Removable Media Workstation) Number (e.g., 1 or 2) |
| -h, --help | Show this help message and exit |
| -i PATH, --input | Input directory |

## Acknowledgments
- rmw_transfer.py is developed based on CollectionSetup.exe by [Matt Adair](mailto:mladair@umich.edu).