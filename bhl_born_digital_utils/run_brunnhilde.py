import os
import shutil
import subprocess
import sys

from bhl_born_digital_utils.config import get_config_setting


def run_brunnhilde(src, accession_number):
    if "win" in sys.platform:
        print("run_brunnhilde cannot be run on Windows")
    else:
        brunnhilde_dir = get_config_setting("brunnhilde")
        cmd = [
            "brunnhilde.py", "-nz",
            src, brunnhilde_dir, accession_number
        ]

        subprocess.call(cmd)

        transfer_metadata_dir = os.path.join(src, "metadata", "submissionDocumentation")
        if not os.path.exists(transfer_metadata_dir):
            os.makedirs(transfer_metadata_dir)

        brunnhilde_reports = os.path.join(brunnhilde_dir, accession_number)
        dst_dir = os.path.join(transfer_metadata_dir, "brunnhilde")
        shutil.copytree(brunnhilde_reports, dst_dir)
