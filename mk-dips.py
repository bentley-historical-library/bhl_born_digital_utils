import argparse
import os
import subprocess

parser = argparse.ArgumentParser(description='Make DIPs from the RipStation (AKA Jackie).')

parser.add_argument('--type', choices = ['data', 'cd', 'dvd'], required=True, help='Pick one: Data CD(s) or DVD(s); audio CD(s); or video-formatted DVD(s)')
parser.add_argument('--src', required=True, help='Input directory')
parser.add_argument('--dst', required=True, help='Output directory')
parser.add_argument('--include', help='Text file with one barcode (to include) per line')
parser.add_argument('--exclude', help='Text file with one barcode (to exclude) per line')

args = parser.parse_args()

if args.type == 'data':
    print 'TO-DO'

elif args.type == 'cd':
 
    include = []
    if args.include and not args.exclude:
        with open(os.path.join(args.include), mode="r") as f:
            for barcode in f:
                include.append(barcode.strip())
            
    elif args.exclude and not args.include:
        exclude = []
        with open(os.path.join(args.exclude), mode="r") as f:
            for barcode in f:
                exclude.append(barcode.strip())
                
        for barcode in os.listdir(os.path.join(args.src)):
            if barcode not in exclude:
                include.append(barcode.strip())
                
    elif args.include and args.exclude:
        exclude = []
        with open(os.path.join(args.exclude), mode="r") as f:
            for barcode in f:
                exclude.append(barcode.strip())
    
        with open(os.path.join(args.include), mode="r") as f:
            for barcode in f:
                if barcode not in exclude:
                    include.append(barcode.strip())
    
    else:
        for barcode in os.listdir(os.path.join(args.src)):
            include.append(barcode)

    for barcode in include:
    
        print 'Concatenating .WAVs for ' + barcode

        # writing temporary input text file
        tracks = [name for name in os.listdir(os.path.join(args.src, barcode)) if name.endswith('.wav')]
        with open(os.path.join(args.src, barcode, 'mylist.txt'), mode='w') as f:
            for track in sorted(tracks):
                f.write("file '" + os.path.join(args.src, barcode, track) + "'\n")
        
        # concatenating
        subprocess.call([
            'ffmpeg',
            '-f',
            'concat', 
            '-i', os.path.join(args.src, barcode, 'mylist.txt'), 
            '-c', 'copy',
            os.path.join(args.dst, barcode + '.wav')
        ])
    
        # deleting temporary input text file
        os.remove(os.path.join(args.src, barcode, 'mylist.txt'))

elif args.type == 'dvd':
    print 'TO-DO'
