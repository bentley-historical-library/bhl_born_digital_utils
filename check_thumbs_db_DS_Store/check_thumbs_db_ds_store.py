import argparse
import os

parser = argparse.ArgumentParser(description='Check Thumbs.db and DS_Store files')
parser.add_argument('-t_off', action="store_true", default=False, help='Turn off deleting Thumbs.db files')
parser.add_argument('-d_off', action="store_true", default=False, help='Turn off deleting .DS_Store files')
parser.add_argument('--src', required=True, help='Target directory')
args = parser.parse_args()

# Reference
# https://github.com/MarcusBarnes/mik/wiki/Cookbook:-Removing-.Thumbs.db-files-from-a-directory
# https://gist.github.com/mattsparks/19a0911999a623a3c302cc29c96b293a


# Function
# Searching for Thumbs.db files (* Recursive)
def search_thumbs_db(src_path):
    print('Searching for Thumbs.db files in "' + src_path + '"')
    for dirpath, dirnames, files in os.walk(src_path):
        for file in files:
            if file == "Thumbs.db":
                file_path = os.path.join(dirpath, file)
                thumbs_db_list.append(file_path)


# Deleting Thumbs.db files (* Recursive)
def delete_thumbs_db():
    for thumbs_db in thumbs_db_list:
        print('Deleting "' + thumbs_db + '"')
        try:
            os.remove(thumbs_db)
        except OSError:
            print('Failed deleting "' + thumbs_db + '"')
            pass
    print('Deleting Done!')


# Searching for .DS_Store files (* Recursive)
def search_ds_store(src_path):
    print('Searching for .DS_Store files in "' + src_path + '"')
    for dirpath, dirnames, files in os.walk(src_path):
        for file in files:
            if file.endswith('.DS_Store'):
                file_path = os.path.join(dirpath, file)
                ds_store_list.append(file_path)


# Deleting .DS_Store files (* Recursive)
def delete_ds_store():
    for ds_store in ds_store_list:
        print('Deleting "' + ds_store + '"')
        try:
            os.remove(ds_store)
        except OSError:
            print('Failed deleting "' + ds_store + '"')
            pass
    print('Deleting Done!')


# Script
thumbs_db_list = []
ds_store_list = []

if args.t_off is False:
    search_thumbs_db(args.src)
    if len(thumbs_db_list) != 0:
        print('Found', len(thumbs_db_list), 'Thumbs.db file(s) in', args.src + '.')
        delete_thumbs_db()
        print()
    else:
        print('Found', len(thumbs_db_list), 'Thumbs.db file in', args.src + '.')
        print()
else:
    pass

if args.d_off is False:
    search_ds_store(args.src)
    if len(ds_store_list) != 0:
        print('Found', len(ds_store_list), '.DS_Store file(s) in', args.src + '.')
        delete_ds_store()
    else:
        print('Found', len(ds_store_list), '.DS_Store file in', args.src + '.')
else:
    pass

if args.t_off is True and args.d_off is True:
    print('What is my purpose? :(')
