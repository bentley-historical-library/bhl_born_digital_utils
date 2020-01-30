import os
import shutil
from subprocess import call, DEVNULL

# Reference
# https://github.com/MarcusBarnes/mik/wiki/Cookbook:-Removing-.Thumbs.db-files-from-a-directory
# https://gist.github.com/mattsparks/19a0911999a623a3c302cc29c96b293a
# https://stackoverflow.com/questions/8529390/is-there-a-quiet-version-of-subprocess-call


def check_os_files(src_path, thumbsdb_off, dsstore_off, desktopdbdf_off, dirs_off):
    filenames_to_delete = ["Thumbs.db", ".DS_Store", "Desktop DB", "Desktop DF"]
    directories_to_delete = [".Trashes", ".Spotlight-V100", ".fseventsd"]

    if thumbsdb_off:
        filenames_to_delete.remove("Thumbs.db")
    if dsstore_off:
        filenames_to_delete.remove(".DS_Store")
    if desktopdbdf_off:
        filenames_to_delete.remove("Desktop DB")
        filenames_to_delete.remove("Desktop DF")
    if dirs_off:
        directories_to_delete = []

    target_lists = search_targets(src_path, filenames_to_delete, directories_to_delete)
    if len(target_lists["files"]) > 0:
        confirm_deletion(src_path, target_lists["files"], filenames_to_delete, target_type="files")
    else:
        print("\nFound no files to delete")
    if len(target_lists["directories"]) > 0:
        confirm_deletion(src_path, target_lists["directories"], directories_to_delete, target_type="directories")
    else:
        print("\nFound no directories to delete")


def search_targets(src_path, filenames_to_delete, directories_to_delete):
    target_lists = {"files": [], "directories": []}
    for root, dirnames, filenames in os.walk(src_path):
        for dirname in dirnames:
            if dirname in directories_to_delete:
                dirpath = os.path.join(root, dirname)
                target_lists["directories"].append(dirpath)

        for filename in filenames:
            if any([fname for fname in filenames_to_delete if filename == fname]):
                filepath = os.path.join(root, filename)
                target_lists["files"].append(filepath)

    return target_lists


def confirm_deletion(src_path, target_list, target_names, target_type):
    print("\nFound {} {} matching the following names: {}".format(len(target_list), target_type, ", ".join(target_names)))
    for target in target_list:
        print(target)

    confirmation = input("\nDo you want to delete all of the above {}? ".format(target_type))
    if confirmation.lower().strip() in ["y", "yes"]:
        delete_targets(src_path, target_list, target_type)


def log_deletion(src_path, deleted_targets, target_type):
    metadata_dir = os.path.join(src_path, "metadata", "submissionDocumentation")
    if not os.path.exists(metadata_dir):
        os.makedirs(metadata_dir)
    logs_file = os.path.join(metadata_dir, "deleted_system_{}.txt".format(target_type))
    with open(logs_file, "w") as f:
        f.write("\n".join(deleted_targets))


def delete_targets(src_path, target_list, target_type):
    deleted_targets = []
    for target in target_list:
        if target_type == "files":
            try:
                call(["attrib", "-H", "-R", "-S", target], stderr=DEVNULL, stdout=DEVNULL)
                os.remove(target)
                deleted_targets.append(target)
            except OSError:
                print("Failed to delete file: {}".format(target))
        elif target_type == "directories":
            try:
                shutil.rmtree(target)
                deleted_targets.append(target)
            except OSError:
                print("Failed to delete directory: {}".format(target))
    print("Deleted {}".format(target_type))
    log_deletion(src_path, deleted_targets, target_type)
