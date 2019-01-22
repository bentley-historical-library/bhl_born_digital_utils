import argparse
import os

from PIL import Image, ImageEnhance

parser = argparse.ArgumentParser(description='Removable Media Workstation (RMW) transfer')
parser.add_argument('-moff', '--metadata_off', action="store_true", default=False, help='Turn off creating bhl_metadata')
parser.add_argument('-noff', '--notice_off', action="store_true", default=False, help='Turn off creating bhl_notices')
parser.add_argument('-src', required=True, help='Accession folder')
parser.add_argument('-rmw', type=int, choices=range(1, 3), required=True,
                    help='Removable Media Workstation (RMW) number')
args = parser.parse_args()

# Reference
# https://stackoverflow.com/questions/8114355/loop-until-a-specific-user-input
# https://stackoverflow.com/questions/13654122/how-to-make-python-get-the-username-in-windows-and-then-implement-it-in-a-script
# https://automatetheboringstuff.com/chapter17/
# https://stackoverflow.com/questions/39424052/how-to-set-coordinates-when-cropping-an-image-with-pil
# http://www.techerator.com/2011/12/how-to-embed-images-directly-into-your-html/
# https://www.base64-image.de/
# https://lindell.me/JsBarcode/
# https://stackoverflow.com/questions/10112614/how-do-i-create-a-multiline-python-string-with-inline-variables


# Function
def create_barcode_dir(src_path):
    barcode = get_input('barcode')

    if os.path.isdir(os.path.join(src_path, barcode)) is False:
        try:
            os.mkdir(os.path.join(src_path, barcode))
            print('Created a folder for', barcode + '.')
        except FileExistsError:
            print(barcode, 'already exists.')
            pass
    else:
        print(barcode, 'already exists.')
        pass

    return barcode


def create_bhl_metadata_dir(src_path, barcode):
    if os.path.isdir(os.path.join(src_path, barcode, 'bhl_metadata')) is False:
        try:
            os.mkdir(os.path.join(src_path, barcode, 'bhl_metadata'))
            print('Created a bhl_metadata folder for', barcode + '.')
        except FileExistsError:
            print(barcode + '\\bhl_metadata', 'already exists.')
            pass
    else:
        print(barcode + '\\bhl_metadata', 'already exists.')
        pass


def get_bhl_metadata_image(src_path, rmw_num, barcode):
    webcam_dir_path = 'C:\\Users\\' + os.getlogin() + '\\Pictures\\Logitech Webcam'
    bhl_metadata_dir_path = os.path.join(src_path, barcode, 'bhl_metadata')

    # Checking if webcam directory is empty
    if len(os.listdir(os.path.join(webcam_dir_path))) != 0:

        # Asking
        decision_result = get_input('delete_webcam_jpg_files')

        # Deleting any images from previous session
        if decision_result is True:
            print('Deleting image files...')
            for dirpath, dirnames, files in os.walk(webcam_dir_path):
                for file in files:
                    print('Deleting "' + file + '"')
                    try:
                        os.remove(os.path.join(dirpath, file))
                    except OSError:
                        print('Failed to delete "' + file + '"')
                        break
            print('Deleting Done!')

        # Keeping
        if decision_result is False:
            print('Any JPG files in the webcam folder will be included in the bhl_metadata folder.')
            pass

    # Checking if webcam directory has new image(s)
    while True:
        input('Take image(s) of removable media and press Enter to continue...')
        if len(os.listdir(os.path.join(webcam_dir_path))) != 0:
            break

    # Moving image(s) to barcode/bhl_metadata and renaming images
    for dirpath, dirnames, files in os.walk(webcam_dir_path):
        files.sort()
        counter = 0
        for file in files:
            os.rename(os.path.join(webcam_dir_path, file),
                      os.path.join(bhl_metadata_dir_path, 'media_' + str(counter) + '.jpg'))
            print('Moved', 'media_' + str(counter) + '.jpg.')
            counter = counter + 1

    # Post-processing image(s)
    for dirpath, dirnames, files in os.walk(bhl_metadata_dir_path):
        for file in files:
            thumb_image = Image.open(os.path.join(bhl_metadata_dir_path, file))

            if rmw_num == 1:  # 1920x1080 >> 1067x600 >> 800x600
                thumb_image = thumb_image.resize((1067, 600)).crop((133, 0, 933, 600))
            if rmw_num == 2:  # 800x600
                pass

            thumb_image = ImageEnhance.Brightness(thumb_image).enhance(1.5)
            thumb_image.save(os.path.join(bhl_metadata_dir_path, file))
            print('Post-processed', file + '.')


def create_notice_of_media_removable(src_path, barcode):
    # Checking
    if os.path.isdir(os.path.join(src_path, 'bhl_notices')) is False:
        try:
            os.mkdir(os.path.join(src_path, 'bhl_notices'))
            print('Created a bhl_notices folder.')
        except FileExistsError:
            pass
    else:
        pass

    # Creating
    notice_html = open(os.path.join(src_path, 'bhl_notices', barcode + '.html'), mode='w')
    notice_html_temp = '''
    <html>
    <head>
        <meta charset="utf-8">
        <title>Notice of Media Removal</title>
        <style type="text/css">
            .logo { object-fit: cover; width: 600px }
            .media { border: 1px solid #000; object-fit: cover; width: 600px }
            body { font-family: sans-serif }
            h1 { font-size: 3em; }
            h3 { font-size: 2em; }
            p { padding: 1.5em ; font-size: 1.5em; }
            </style>
        <script src="https://cdn.jsdelivr.net/jsbarcode/3.6.0/JsBarcode.all.min.js"></script>
    </head>
    
    <body>
        <div><img class="logo" src="data:image/png;base64,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"/></div>
        <h1>Notice of Media Removal</h1>
        <div><img class="media" src="%s"/></div>
        <p>To ensure the long-term preservation of and access to digital content, the Bentley Historical Library removed a piece of digital storage media from this location and transferred the files to a digital repository. Please see this item location in this collection/record group's online finding aid for additional information about this material; if open for research, the finding aid will include a hyperlink to the content.</p>
        <h3>Barcode:</h3>
        <img id="barcode"/>
        <script type="text/javascript">JsBarcode("#barcode", "%s", {format: "codabar", width: "2", margin: "0"});</script>
    </body>
    </html>''' % (os.path.join(src_path, barcode, 'bhl_metadata', 'media_0.jpg'), barcode)
    notice_html.write(notice_html_temp)
    notice_html.close()
    print('Created a notice of media removable for', barcode + '.')


def get_input(input_type):
    if input_type == 'barcode':
        while True:
            barcode = input('Barcode? >>> ').replace(' ', '')
            if barcode.isdigit() is False:
                print('Your barcode is not a number.')
            if len(barcode) != 14:
                print('Your barcode is not a 14-digit number.')
            if barcode.isdigit() is True and len(barcode) == 14:
                break
            print('Please try again.')
            print()

        return barcode

    if input_type == 'delete_webcam_jpg_files':
        while True:
            print('The webcam folder contains JPG files.')
            print('Do you want to delete all of these images? (y/n/show me)')
            decision_input = input('>>> ').replace(' ', '').lower()
            if decision_input == 'y':
                decision = True
                break
            if decision_input == 'n':
                decision = False
                break
            if decision_input == 'showme':
                os.startfile('C:\\Users\\' + os.getlogin() + '\\Pictures\\Logitech Webcam')
            print('Please try again.')
            print()

        return decision

    if input_type == 'more barcode':
        while True:
            decision_input = input('More removable media? (y/n) >>> ').replace(' ', '').lower()
            if decision_input == 'y':
                decision = True
                break
            if decision_input == 'n':
                decision = False
                break
            print('Please try again.')
            print()

        return decision


# Script
while True:
    barcode = create_barcode_dir(args.src)
    print()

    if args.metadata_off is False:
        create_bhl_metadata_dir(args.src, barcode)
        get_bhl_metadata_image(args.src, args.rmw, barcode)
        print()

    if args.notice_off is False:
        create_notice_of_media_removable(args.src, barcode)
        print()

    decision = get_input('more barcode')
    if decision is False:
        break
