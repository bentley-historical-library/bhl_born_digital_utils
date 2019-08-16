import argparse
import os
from subprocess import call

# Start in drive where script is located
# cd to folder where script is located & then type:
# python runbe.py -i "<drag/source/path>"
# You must encapsulate the path in double quotes in the command line!

parser = argparse.ArgumentParser(description='Run bulk_extractor.exe from the command line.')
parser.add_argument('-i', '--input', required=True, help='Input directory')
args = parser.parse_args()

def run_extractor(src):
    # print("source >>> " + src +'\n')
    top_folder = os.path.dirname(os.getcwd())
        # The results folder goes top level of the directory where this script is running from.
    dst = input("Enter a NEW folder name >>> ").replace(' ', '')
    new_folder = os.path.join(top_folder, dst)
    bulk_extractor = "C:\\BHL\\Utilities\\Bulk Extractor 1.6.0-dev\\bulk_extractor.exe"
    call([bulk_extractor, "-S" "ssn_mode=1", "-E" "accts", "-x" "exif", "-o", new_folder, "-R", src])
        # -o <new folder> must come before -R <source folder>

    print("\nThe results folder located here >>> " + new_folder + '\n')

run_extractor(args.input)
