import argparse
import os

parser = argparse.ArgumentParser(description='Check empty folders')
parser.add_argument('--src', required=True, help='Target directory')
args = parser.parse_args()


# Function
# Check for empty barcode folders (* Not recursive)
def check_empty_folder(src_path):
    print('Checking empty folders in', src_path)
    for dirpath, dirnames, files in os.walk(src_path):
        for dirname in dirnames:
            if len(os.listdir(os.path.join(dirpath, dirname))) == 0:
                print('>>>', dirpath + '\\' + dirname, 'is empty')
#            else:
#                print(dirpath + '\\' + dirname, 'has files')
        break
    print('Done!')
    print()


# Check for empty files in a barcode folder (* Not recursive)
def check_empty_file(src_path):
    directory_list = []
    print('Checking empty files in', src_path)
    for dirname in os.listdir(src_path):
        if os.path.isdir(os.path.join(src_path, dirname)):
            directory_list.append(dirname)

    for dirname in directory_list:
        for dirpath, dirnames, files in os.walk(src_path + '\\' + dirname):
            print('Checking empty files in', dirpath)
            for file in files:
                file_path = os.path.join(dirpath, file)
                file_size = os.path.getsize(file_path)
                if file_size == 0:
                    print('>>>', dirpath + '\\' + file + ' is empty')
        break
    print('Done!')


# Script
check_empty_folder(args.src)
check_empty_file(args.src)
