import os
import shutil

from PIL import Image

from bhl_born_digital_utils.config import get_config_setting

# Reference
# https://stackoverflow.com/questions/8114355/loop-until-a-specific-user-input
# https://stackoverflow.com/questions/13654122/how-to-make-python-get-the-username-in-windows-and-then-implement-it-in-a-script
# https://automatetheboringstuff.com/chapter17/
# https://stackoverflow.com/questions/39424052/how-to-set-coordinates-when-cropping-an-image-with-pil
# http://www.techerator.com/2011/12/how-to-embed-images-directly-into-your-html/
# https://www.base64-image.de/
# https://lindell.me/JsBarcode/
# https://stackoverflow.com/questions/10112614/how-do-i-create-a-multiline-python-string-with-inline-variables


def verify_barcode(barcode):
    if barcode.isdigit() and len(barcode) == 14:
        return True
    else:
        if not barcode.isdigit():
            print("Your barcode is not a number")
        if len(barcode) != 14:
            print("Your barcode is not a 14-digit number")
        return False


def get_barcode():
    barcode = input("Scan a barcode: ")
    while not verify_barcode(barcode):
        print("Please try again.")
        barcode = get_barcode()
    return barcode


def create_barcode_dir(src_path, barcode):
    barcode_dir = os.path.join(src_path, barcode)
    check_and_create_dir(barcode_dir)


def create_bhl_metadata_dir(src_path, barcode):
    bhl_metadata_dir = os.path.join(src_path, barcode, "bhl_metadata")
    check_and_create_dir(bhl_metadata_dir)


def create_bhl_notices_dir(src_path):
    bhl_notices_dir = os.path.join(src_path, "bhl_notices")
    check_and_create_dir(bhl_notices_dir)


def check_and_create_dir(dirpath):
    if not os.path.exists(dirpath):
        os.mkdir(dirpath)
        print("Created directory {}".format(dirpath))
    else:
        print("Directory already exists at {}".format(dirpath))


def delete_webcam_files(webcam_dir):
    print("The webcam directory contains existing files")
    if len(os.listdir(webcam_dir)) < 10:
        for filename in os.listdir(webcam_dir):
            if filename.lower().endswith("jpg"):
                print(filename)
    else:
        print("The directory has more than ten files. Open {} to check what they are.".format(webcam_dir))
    delete_them = input("Do you want to delete these images? (y/n): ")
    if delete_them.lower().strip() in ["y", "yes"]:
        for root, _, filenames in os.walk(webcam_dir):
            for filename in filenames:
                if filename.lower().endswith("jpg"):
                    filepath = os.path.join(root, filename)
                    print("Deleting {}".format(filepath))
                    try:
                        os.remove(filepath)
                    except OSError:
                        print("Could not delete {}".format(filepath))
        print("Files in the webcam directory have been deleted.")
    else:
        print("Any JPG files in the webcam folder will be included in the bhl_metadata folder.")


def check_webcam_dir(webcam_dir):
    input("Take image(s) of removable media and press Enter to continue...")
    if len(os.listdir(webcam_dir)) == 0:
        print("Sorry, couldn't find any images in {}".format(webcam_dir))
        take_images = input("Do you want to take image(s)? (y/n): ")
        if take_images.lower().strip() in ["y", "yes"]:
            return check_webcam_dir(webcam_dir)
        else:
            return False
    else:
        return True


def move_and_post_process_images(webcam_dir, bhl_metadata_dir):
    move_images(webcam_dir, bhl_metadata_dir)
    post_process_images(bhl_metadata_dir)


def move_images(webcam_dir, bhl_metadata_dir):
    counter = 0
    for root, dirnames, filenames in os.walk(webcam_dir):
        for filename in sorted(filenames):
            if filename.lower().endswith("jpg"):
                image_src_path = os.path.join(webcam_dir, filename)
                image_dst_path = os.path.join(bhl_metadata_dir, "media_{}.jpg".format(counter))
                shutil.move(image_src_path, image_dst_path)
                print("Moved {} to {}".format(image_src_path, image_dst_path))
                counter += 1


def post_process_images(bhl_metadata_dir):
    for filename in os.listdir(bhl_metadata_dir):
        if filename.endswith("jpg"):
            image_path = os.path.join(bhl_metadata_dir, filename)
            img = Image.open(image_path)
            area = (880, 0, 3100, 1675)
            img = img.crop(area)
            img.save(image_path)
            print("Processed image {}".format(filename))


def get_bhl_metadata_images(src_path, barcode):
    webcam_dir = get_config_setting("webcam_dir")
    bhl_metadata_dir = os.path.join(src_path, barcode, "bhl_metadata")
    # check if the webcam directory has images from a previous session
    existing_files = os.listdir(webcam_dir)
    if any([filename for filename in existing_files if filename.lower().endswith("jpg")]):
        delete_webcam_files(webcam_dir)

    images_exist = check_webcam_dir(webcam_dir)
    if images_exist:
        move_and_post_process_images(webcam_dir, bhl_metadata_dir)


def create_notice(src_path, barcode):
    bhl_notices_dir = os.path.join(src_path, "bhl_notices")
    media_path = "../{}/bhl_metadata/media_0.jpg".format(barcode)
    base_dir = os.path.abspath(os.path.dirname(__file__))
    lib_dir = os.path.join(base_dir, "lib")
    base_64_logo_txt = os.path.join(lib_dir, "base_64_logo.txt")
    notice_template = os.path.join(lib_dir, "notice_html_template.html")
    with open(base_64_logo_txt, "r") as f:
        base_64_logo = f.read()

    with open(notice_template, "r") as f:
        notice_html = f.read() \
                    .replace("{{ BASE_64_LOGO }}", base_64_logo) \
                    .replace("{{ MEDIA_PATH }}", media_path) \
                    .replace("{{ BARCODE }}", barcode)

    notice_html_file = os.path.join(bhl_notices_dir, "{}.html".format(barcode))
    with open(notice_html_file, "w") as f:
        f.write(notice_html)
    print("Created notice of removable media for {}.".format(barcode))


def add_removable_media(src_path, metadata_off, notices_off):
    barcode = get_barcode()
    create_barcode_dir(src_path, barcode)
    if not metadata_off:
        create_bhl_metadata_dir(src_path, barcode)
        get_bhl_metadata_images(src_path, barcode)

    if not notices_off:
        create_bhl_notices_dir(src_path)
        create_notice(src_path, barcode)

    create_another_transfer = input("Do you have more removable media to transfer? (y/n): ")
    if create_another_transfer.lower().strip() in ["y", "yes"]:
        add_removable_media(src_path, metadata_off, notices_off)


def create_rmw_transfer(src_path, metadata_off, notices_off):
    check_and_create_dir(src_path)
    bhl_inventory = os.path.join(src_path, "bhl_inventory.csv")
    if not os.path.exists(bhl_inventory):
        base_dir = os.path.abspath(os.path.dirname(__file__))
        bhl_inventory_template = os.path.join(base_dir, "lib", "bhl_inventory", "bhl_inventory.csv")
        shutil.copy(bhl_inventory_template, bhl_inventory)
        print("Copied bhl_inventory.csv to {}".format(src_path))
    add_removable_media(src_path, metadata_off, notices_off)
