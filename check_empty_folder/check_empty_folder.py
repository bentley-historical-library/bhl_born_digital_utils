import argparse
import os

parser = argparse.ArgumentParser(description='Check empty folders.')
parser.add_argument('--src', required=True, help='Input directory')
args = parser.parse_args()


def check_empty_folder(src_path):
    for dirpath, dirnames, files in os.walk(src_path):
        print('Checking empty folders in ', dirpath)
        for dirname in dirnames:
            if len(os.listdir(os.path.join(dirpath, dirname))) == 0:
                print(dirpath + '\\' + dirname, 'is empty')
#            else:
#                print(dirpath + '\\' + dirname, 'has files')
        break


check_empty_folder(args.src)
