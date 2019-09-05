import os
import string

# Borrowed heavily from https://github.com/artefactual/archivematica/blob/stable/1.9.x/src/MCPClient/lib/clientScripts/sanitize_names.py
valid = string.ascii_letters + string.digits + r"-_.()#,&[]%$\+{}~! "
replacement_char = "_"


class RenameFailed(Exception):
    def __init__(self, code):
        self.code = code


def rename_files(src_path):
    targets = get_targets(src_path)
    confirm_renaming(targets)


def get_targets(src_path):
    files_to_rename = []
    for root, _, filenames in os.walk(src_path):
        for filename in filenames:
                if any([c for c in filename if c not in valid]):
                    filepath = os.path.join(root, filename)
                    files_to_rename.append(filepath)
    return files_to_rename


def confirm_renaming(targets):
    print("*** THE FOLLOWING INVALID FILENAMES HAVE BEEN FOUND ***")
    print("\n".join(targets))
    confirm_rename = input("Rename files?: ")
    if confirm_rename.lower().strip() in ["y", "yes"]:
        n = 1
        for target in targets:
            filename = os.path.basename(target)
            dirname = os.path.dirname(target)
            sanitized_name = sanitize_name(filename)
            fileTitle, fileExt = os.path.splitext(sanitized_name)
            sanitized_path = os.path.join(dirname, fileTitle + fileExt)
            while os.path.exists(sanitized_path):
                sanitized_path = os.path.join(dirname, fileTitle + "_" + str(n) + fileExt)
                n += 1
            exit_status = os.rename(target, sanitized_path)
            if exit_status:
                raise RenameFailed(exit_status)
            print("{} renamed to {}".format(target, sanitized_path))


def sanitize_name(filename):
    sanitized_name = ""
    for c in filename:
        if c in valid:
            sanitized_name += c
        else:
            sanitized_name += replacement_char
    return sanitized_name
