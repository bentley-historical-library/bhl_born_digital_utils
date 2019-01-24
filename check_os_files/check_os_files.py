import argparse
import os
from subprocess import call, DEVNULL

parser = argparse.ArgumentParser(description='Check Thumbs.db and DS_Store files')
parser.add_argument('-t', '--thumbsdb_off', action="store_true", default=False,
                    help='Turn off deleting Thumbs.db files')
parser.add_argument('-ds', '--dsstore_off', action="store_true", default=False,
                    help='Turn off deleting .DS_Store files')
parser.add_argument('-df', '--desktopdbdf_off', action="store_true", default=False,
                    help='Turn off deleting Desktop DB and Desktop DF files')
parser.add_argument('-src', required=True, help='Target directory')
args = parser.parse_args()

# Reference
# https://github.com/MarcusBarnes/mik/wiki/Cookbook:-Removing-.Thumbs.db-files-from-a-directory
# https://gist.github.com/mattsparks/19a0911999a623a3c302cc29c96b293a
# https://stackoverflow.com/questions/8529390/is-there-a-quiet-version-of-subprocess-call


# Function
# Searching for target files (* Recursive)
def search_target(src_path, target):
    target_list.clear()
    print('Searching for', target, 'files in', src_path)
    for dirpath, dirnames, files in os.walk(src_path):
        for file in files:
            if file.endswith(target):
                file_path = os.path.join(dirpath, file)
                target_list.append(file_path)


# Showing search result for target files and confirming user with deleting those files
def confirm_delete_target(target):
    if len(target_list) != 0:
        print('Found', len(target_list), target, 'file(s) in', args.src)
        while True:
            decision_input = input('Do you want to delete all ' + target + ' file(s)? (y/n) >>> ').replace(' ', '').lower()
            if decision_input == 'y':
                delete_target()
                print()
                break
            if decision_input == 'n':
                print()
                break
            print('Please answer in y or n.')
    else:
        print('Found', len(target_list), target, 'file in', args.src)
        print()


# Deleting target files (* Recursive)
def delete_target():
    for target in target_list:
        print('Deleting', target)
        try:
            call(["attrib", "-R", "-S", target], stderr=DEVNULL, stdout=DEVNULL)
            os.remove(target)
        except OSError:
            print('Failed to delete', target)
            pass
    print('Deleting Done!')


# Script
target_list = []

if args.thumbsdb_off is False:
    search_target(args.src, 'Thumbs.db')
    confirm_delete_target('Thumbs.db')

if args.dsstore_off is False:
    search_target(args.src, '.DS_Store')
    confirm_delete_target('.DS_Store')

if args.desktopdbdf_off is False:
    search_target(args.src, 'Desktop DB')
    confirm_delete_target('Desktop DB')
    search_target(args.src, 'Desktop DF')
    confirm_delete_target('Desktop DF')
