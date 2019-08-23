import os
import subprocess
import sys


def unhide_folders(src_path):
    if "win" in sys.platform:
        for root, dirnames, _ in os.walk(src_path):
            for dirname in dirnames:
                dirpath = os.path.join(root, dirname)
                subprocess.call(["attrib", "-H", "-S", dirpath])
        print("All folders are now unhidden")
    else:
        print("unhide_folders is intended to be run from a Windows machine")
