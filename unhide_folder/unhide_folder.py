import argparse
import os
from subprocess import call

import win32api
import win32con

parser = argparse.ArgumentParser(description='Check missing folders')
parser.add_argument('-i', '--input', required=True, help='Input directory')
args = parser.parse_args()


def unhide_folder(src_path):
    unhidden_list = []
    for dirpath, dirnames, files in os.walk(src_path):
        for dirname in dirnames:
            attribute = win32api.GetFileAttributes(dirpath + '\\' + dirname)
            try:
                if attribute & (win32con.FILE_ATTRIBUTE_SYSTEM | win32con.FILE_ATTRIBUTE_HIDDEN):  # if folder is hidden
                    call(["attrib", "-H", "-S", dirpath + '\\' + dirname])
                    unhidden_list.append(dirname)
                    print(str(dirname) + ' is no longer hidden')

                else:  # if folder is not hidden
                    print(str(dirname) + " is already unhidden")
                    pass
            except:
                print(str(dirname) + " FAILED to unhide")
        break
    print('Found ' + str(len(unhidden_list)) + ' hidden folders')


unhide_folder(args.input)