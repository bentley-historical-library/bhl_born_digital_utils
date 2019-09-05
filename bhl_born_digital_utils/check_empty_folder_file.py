import os


def check_empty_folder_file(src_path):
    print("Checking for empty folders and files in {}".format(src_path))
    empty_folders = []
    empty_files = []
    for dirpath, dirnames, filenames in os.walk(src_path):
        # check for empty barcode folders
        for dirname in dirnames:
            if len(os.listdir(os.path.join(dirpath, dirname))) == 0:
                empty_folders.append(os.path.join(dirpath, dirname))

        # check for 0 byte files in a barcode folder
        for filename in filenames:
            file_path = os.path.join(dirpath, filename)
            file_size = os.path.getsize(file_path)
            if file_size == 0:
                empty_files.append(file_path)

    if len(empty_folders) > 0:
        print("*** EMPTY FOLDERS FOUND ***")
        print("\n".join(empty_folders))

    if len(empty_files) > 0:
        print("\n")
        print("*** EMPTY FILES FOUND ***")
        print("\n".join(empty_files))
