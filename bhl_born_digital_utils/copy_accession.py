from datetime import datetime
import os
import platform
import subprocess

# Resource: https://www.computerhope.com/robocopy.htm


def get_copy_command(src, dst):
    if "windows" in platform.platform().lower():
        return get_robocopy_command(src, dst)
    else:
        return get_rsync_command(src, dst)


def get_log_filepath(accession_number, copy_tool):
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    log_dir = os.path.join(base_dir, "logs")
    if not os.path.exists(log_dir):
        os.mkdir(log_dir)
    accession_dir = os.path.join(log_dir, accession_number)
    if not os.path.exists(accession_dir):
        os.mkdir(accession_dir)
    log_name = accession_number + "_" + datetime.now().strftime("%Y%m%d%H%M%S") + "_" + copy_tool
    log_path = os.path.join(accession_dir, "{}.txt".format(log_name))
    return log_path


def get_robocopy_command(src, dst):
    accession_number = os.path.split(src)[-1]
    destination = os.path.join(dst, accession_number)
    log_path = get_log_filepath(accession_number, "robocopy")
    log_opts = "/log:{}".format(log_path)
    if platform.release() == "10":
        directory_opts = "DAT"
    else:
        directory_opts = "T"
    return [
            "robocopy", src, destination, "/e", "/copy:DAT",
            "/dcopy:{}".format(directory_opts), log_opts, "/tee"
            ]


def get_rsync_command(src, dst):
    accession_number = os.path.split(src)[-1]
    log_path = get_log_filepath(accession_number, "rsync")
    log_opts = "--log-file={}".format(log_path)
    return [
            'rsync', '-t', '--protect-args', '-vv',
            '-r', src, dst, log_opts
            ]


def copy_accession(src, dst):
    copy_command = get_copy_command(src, dst)
    subprocess.call(copy_command)
