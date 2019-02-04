import argparse
import os
from subprocess import call
import win32api, win32con


parser = argparse.ArgumentParser(description='Check missing folders')
parser.add_argument('--src', required=True, help='Target directory')
args = parser.parse_args()

def unhide_folders(src_path):
	unhidden_list = []
  
	for dirpath, dirnames, files in os.walk(src_path):
		for dirname in dirnames:
			attribute = win32api.GetFileAttributes(dirpath + '\\' + dirname)
			try:
				if attribute & (win32con.FILE_ATTRIBUTE_SYSTEM | win32con.FILE_ATTRIBUTE_HIDDEN):   #if folder is hidden
					call(["attrib", "-s", "-h", dirpath + '\\' + dirname])
					unhidden_list.append(dirname)
					print(str(dirname) + ' is no longer hidden')
			
				else:  #if folder is not hidden
					print(str(dirname) + " is already unhidden")
					pass
			except:
				print(str(dirname) + " FAILED to unhide")
		break
	print('Found ' + str(len(unhidden_list)) + ' hidden folders')


unhide_folders(args.src)	