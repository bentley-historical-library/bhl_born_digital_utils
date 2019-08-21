import argparse
import os
from subprocess import call, DEVNULL

parser = argparse.ArgumentParser(description='Check Thumbs.db,  DS_Store, Desktop DB, and Desktop DF files')
parser.add_argument('-b', '--thumbsdb_off', action="store_true", default=False,
                    help='Turn off deleting Thumbs.db files')
parser.add_argument('-e', '--dsstore_off', action="store_true", default=False,
                    help='Turn off deleting .DS_Store files')
parser.add_argument('-f', '--desktopdbdf_off', action="store_true", default=False,
                    help='Turn off deleting Desktop DB and Desktop DF files')
parser.add_argument('-i', '--input', required=True, help='Input directory')
args = parser.parse_args()

# Reference
# https://github.com/MarcusBarnes/mik/wiki/Cookbook:-Removing-.Thumbs.db-files-from-a-directory
# https://gist.github.com/mattsparks/19a0911999a623a3c302cc29c96b293a
# https://stackoverflow.com/questions/8529390/is-there-a-quiet-version-of-subprocess-call


# Function
# Searching for target files (* Recursive)
def search_targets(src_path, targets):
    target_list = []
    print('Searching for', ", ".join(targets), 'files in', src_path)
    for dirpath, dirnames, files in os.walk(src_path):
        for file in files:
            if any([target for target in targets if file.endswith(target)]):
                file_path = os.path.join(dirpath, file)
                target_list.append(file_path)
    return target_list


# Showing search result for target files and confirming user with deleting those files
def confirm_delete_targets(src_path, targets, target_list):
    if len(target_list) != 0:
        print('Found', len(target_list), ", ".join(targets), 'file(s) in', src_path)
        while True:
            decision_input = input('Do you want to delete all ' + ", ".join(targets) + ' file(s)? (y/n) >>> ').replace(' ', '').lower()
            if decision_input == 'y':
                delete_targets(target_list)
                print()
                break
            if decision_input == 'n':
                print()
                break
            print('Please answer in y or n.')
    else:
        print('Found', len(target_list), ", ".join(targets), 'file in', src_path)
        print()


# Deleting target files (* Recursive)
def delete_targets(target_list):
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
file_extensions_to_delete = ["Thumbs.db", ".DS_Store", "Desktop DB", "Desktop DF"]
args_to_file_extensions = {
                    "thumbsdb_off": ["Thumbs.db"],
                    "dsstore_off": [".DS_Store"],
                    "desktopdbdf_off": ["Desktop DB", "Desktop DF"]
                    }

for arg, value in vars(args).items():
    if value is True and arg in args_to_file_extensions.keys():
        for file_extension in args_to_file_extensions[arg]:
            file_extensions_to_delete.remove(file_extension)

if len(file_extensions_to_delete) > 0:
    target_list = search_targets(args.input, file_extensions_to_delete)
    confirm_delete_targets(args.input, file_extensions_to_delete, target_list)
