import argparse
import os
from subprocess import call

# This is used to robocopy new transfers to the R: or S: drive depending on your computer.
# Create a new folder in the R: drive with the name as the accession number BEFORE you robocopy.

# Resources for Windows 10 PowerShell:
# https://www.computerhope.com/robocopy.htm
# https://docs.microsoft.com/en-us/windows-server/administration/windows-commands/robocopy

parser = argparse.ArgumentParser(description='Remove A/V DIPs from the RMLC spreadsheet.')
parser.add_argument('-i', '--input', required=True, help='Input directory')
parser.add_argument('-o', '--output', required=True, help='New output directory')
args = parser.parse_args()

print("\nWelcome to Robocopy for Windows 10!\n") # Updated the script 2019-10-10

def robocopy_directory(rmw_dir, new_dir):
    accession_num = input("Please enter the accession number >>> ")
    log_path = os.path.join(new_dir, str(accession_num) + ".txt")
        # Making sure the log is placed within the robocopied directory.
    log_name = "/log:"+ log_path
    call(["robocopy", rmw_dir, new_dir, "/e", "/copy:DAT", "/dcopy:T", log_name, "/tee"])
        # robocopy <Source> <Destination> /e /copy:DAT /dcopy:T /log:<LogFile> /tee

robocopy_directory(args.input, args.output)
