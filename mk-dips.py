import argparse
import os
import subprocess
import re
import sys

parser = argparse.ArgumentParser(description = 'Make DIPs from the RipStation (AKA Jackie).')

parser.add_argument('--type', choices = ['cd', 'dvd'], required = True, help='Pick one: Data CD(s) or DVD(s); audio CD(s); or video-formatted DVD(s)')
parser.add_argument('--src', required = True, help = 'Input directory')
parser.add_argument('--dst', required = True, help = 'Output directory')
parser.add_argument('--include', help = 'Text file with one barcode (to include) per line')
parser.add_argument('--exclude', help = 'Text file with one barcode (to exclude) per line')

args = parser.parse_args()

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
    
        print '\nMaking .WAVs for barcode ' + barcode

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
        
    print "\nAlright, we're done!"

elif args.type == 'dvd':

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
    
        dvd = False
        for name in os.listdir(os.path.join(args.src, barcode)):
            if os.path.splitext(name)[1].startswith('.iso'):
                dvd = True
                
        if dvd == False:
            
            print 'Not making .MP4s for barcode ' + barcode + '--not a DVD!'
        
        else:
            
            for name in os.listdir(os.path.join(args.src, barcode)):
                if os.path.splitext(name)[1].startswith('.iso'):
                
                    cmd = [
                        os.path.join('HandBrakeCLI-1.0.7-win-x86_64', 'HandBrakeCLI.exe'),
                        '-i', os.path.join(args.src, barcode, name),
                        '-t', '0'
                    ]
                    # https://www.saltycrane.com/blog/2008/09/how-get-stdout-and-stderr-using-python-subprocess-module/
                    p = subprocess.Popen(cmd, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
                    output = p.stdout.read()
                    
                    match = re.findall('scan: DVD has (\d+) title\(s\)', output)
                    
                    title_count = 1
                    if match:
                        title_count = int(match[0])
                        
                    if title_count == 1:
                        print '\nMaking .MP4 for ' + barcode

                        cmd = [
                            os.path.join('HandBrakeCLI-1.0.7-win-x86_64', 'HandBrakeCLI.exe'),
                            '-Z', 'High Profile',
                            '-i', os.path.join(args.src, barcode, name),
                            '-o', os.path.join(args.dst, os.path.splitext(name)[0] + '.mp4')
                        ]
                        subprocess.call(cmd)
                    
                    else:
                        count = 1
                        while count <= title_count:
                            print '\nMaking .MP4 for title ' + str(count) + ' of ' + str(title_count)
                            
                            cmd = [
                                os.path.join('HandBrakeCLI-1.0.7-win-x86_64', 'HandBrakeCLI.exe'),
                                '--title', str(count),
                                '-Z', 'High Profile',
                                '-i', os.path.join(args.src, barcode, name),
                                '-o', os.path.join(args.dst, os.path.splitext(name)[0] + '-' + str(count) + '.mp4')
                            ]
                            subprocess.call(cmd)
                            count += 1
        
    print "\nAlright, we're done!"
