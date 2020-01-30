import csv
import os
import re
import shutil

# Borrowed heavily from https://github.com/artefactual/archivematica/blob/stable/1.10.x/src/MCPClient/lib/clientScripts/sanitize_names.py
ALLOWED_CHARS = re.compile(r"[^a-zA-Z0-9\-_\.\(\)#,&%\$\{\}~! ]")
REPLACEMENT_CHAR = "_"


def rename_files(src_path):
    dirs_to_rename, files_to_rename = get_targets(src_path)
    if len(dirs_to_rename) > 0 or len(files_to_rename) > 0:
        confirm_renaming(src_path, dirs_to_rename, files_to_rename)
    else:
        print("No targets to rename were found")


def get_targets(src_path):
    dirs_to_rename = []
    files_to_rename = []
    for old_path, sanitized_path, is_dir, is_target in recursively_get_targets(src_path):
        if is_target:
            if is_dir:
                dirs_to_rename.append((old_path, sanitized_path))
            else:
                files_to_rename.append((old_path, sanitized_path))
    return dirs_to_rename, files_to_rename


def recursively_get_targets(src_path):
    for dir_entry in os.scandir(src_path):
        is_dir = dir_entry.is_dir()

        start_path = dir_entry.path
        basename = os.path.basename(start_path)
        sanitized_name = ALLOWED_CHARS.sub(REPLACEMENT_CHAR, basename)
        sanitized_path = os.path.join(src_path, sanitized_name)

        is_target = sanitized_path != start_path

        yield start_path, sanitized_path, is_dir, is_target

        if is_dir:
            for result in recursively_get_targets(start_path):
                yield result


def log_renaming(src_path, renamed_paths):
    metadata_dir = os.path.join(src_path, "metadata", "submissionDocumentation")
    if not os.path.exists(metadata_dir):
        os.makedirs(metadata_dir)
    logs_file = os.path.join(metadata_dir, "renamed_files_and_directories.csv")
    if not os.path.exists(logs_file):
        with open(logs_file, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["original_path", "renamed_path"])
            writer.writerows(renamed_paths)
    else:
        with open(logs_file, "a", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerows(renamed_paths)


def confirm_renaming(src_path, dirs_to_rename, files_to_rename):
    if len(dirs_to_rename) > 0:
        print("*** DIRECTORIES WILL BE RENAMED AS FOLLOWS ***")
        for old_path, sanitized_path in dirs_to_rename:
            print("{} --> {}".format(old_path, sanitized_path))
        print("\n\n")
    if len(files_to_rename) > 0:
        print("*** FILES WILL BE RENAMED AS FOLLOWS ***")
        for old_path, sanitized_path in files_to_rename:
            print("{} --> {}".format(old_path, sanitized_path))
        print("\n\n")

    confirm_rename = input("Rename files and/or directories? (y/n): ")
    if confirm_rename.lower().strip() in ["y", "yes"]:
        # reverse the lists so that files and directories deeper in the tree get renamed first
        dirs_to_rename.reverse()
        files_to_rename.reverse()
        rename_paths(src_path, files_to_rename)
        rename_paths(src_path, dirs_to_rename)


def rename_paths(src_path, paths):
    n = 1
    renamed_paths = []
    for old_path, new_path in paths:
        dirname = os.path.dirname(old_path)
        basename = os.path.basename(new_path)
        filename, fileext = os.path.splitext(basename)
        sanitized_path = os.path.join(dirname, filename + fileext)
        while os.path.exists(sanitized_path):
            sanitized_path = os.path.join(dirname, filename + REPLACEMENT_CHAR + str(n) + fileext)
            n += 1
        shutil.move(old_path, sanitized_path)
        renamed_paths.append([old_path, sanitized_path])
    log_renaming(src_path, renamed_paths)
