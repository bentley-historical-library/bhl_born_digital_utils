import os
import re
import shutil

# Borrowed heavily from https://github.com/artefactual/archivematica/blob/stable/1.10.x/src/MCPClient/lib/clientScripts/sanitize_names.py
ALLOWED_CHARS = re.compile(r"[^a-zA-Z0-9\-_\.\(\)#,&%\$\{\}~! ]")
REPLACEMENT_CHAR = "_"


def rename_files(src_path):
    dirs_to_rename, files_to_rename = get_targets(src_path)
    confirm_renaming(dirs_to_rename, files_to_rename)


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


def confirm_renaming(dirs_to_rename, files_to_rename):
    print("*** DIRECTORIES WILL BE RENAMED AS FOLLOWS ***")
    for old_path, sanitized_path in dirs_to_rename:
        print("{} --> {}".format(old_path, sanitized_path))
    print("\n\n")
    print("*** FILES WILL BE RENAMED AS FOLLOWS ***")
    for old_path, sanitized_path in files_to_rename:
        print("{} --> {}".format(old_path, sanitized_path))

    confirm_rename = input("Rename files? (y/n): ")
    if confirm_rename.lower().strip() in ["y", "yes"]:
        # reverse the lists so that files and directories deeper in the tree get renamed first
        dirs_to_rename.reverse()
        files_to_rename.reverse()
        rename_paths(files_to_rename)
        rename_paths(dirs_to_rename)


def rename_paths(paths):
    n = 1
    for old_path, new_path in paths:
        dirname = os.path.dirname(old_path)
        basename = os.path.basename(new_path)
        filename, fileext = os.path.splitext(basename)
        sanitized_path = os.path.join(dirname, filename + fileext)
        while os.path.exists(sanitized_path):
            sanitized_path = os.path.join(dirname, filename + REPLACEMENT_CHAR + str(n) + fileext)
            n += 1
        shutil.move(old_path, sanitized_path)
