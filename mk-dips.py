import argparse
import os
import subprocess
import re
import sys


parser = argparse.ArgumentParser(description = 'Make A/V DIPs from the RipStation (AKA Jackie).')

parser.add_argument('--type', choices = ['cd', 'dvd'], required = True, help='Pick one: audio CD(s) or video-formatted DVD(s)')
parser.add_argument('--src', required = True, help = 'Input directory')
parser.add_argument('--dst', required = True, help = 'Output directory')
parser.add_argument('--include', help = 'Text file with one barcode (to include) per line')
parser.add_argument('--exclude', help = 'Text file with one barcode (to exclude) per line')

args = parser.parse_args()


# functions
def get_include(src, include = '', exclude = ''):
    
    include_list = []
    
    if include:
        with open(os.path.join(include), mode="r") as f:
            for barcode in f:
                include_list.append(barcode.strip())
            
    elif exclude:
        exclude_list = []
        with open(os.path.join(exclude), mode="r") as f:
            for barcode in f:
                exclude_list.append(barcode.strip())
                
        for barcode in os.listdir(os.path.join(src)):
            if barcode not in exclude_list:
                include_list.append(barcode.strip())
                
    else:
        for barcode in os.listdir(os.path.join(src)):
            include_list.append(barcode)
            
    return include_list
    
def mk_wav(src, barcode, dst):
    print 'Making .WAVs for barcode ' + barcode

    # writing temporary input text file
    tracks = [name for name in os.listdir(os.path.join(src, barcode)) if name.endswith('.wav')]
    with open(os.path.join(src, barcode, 'mylist.txt'), mode='w') as f:
        for track in sorted(tracks):
            f.write("file '" + os.path.join(src, barcode, track) + "'\n")
    
    # concatenating
    cmd = [
        'ffmpeg',
        '-f',
        'concat', 
        '-i', os.path.join(src, barcode, 'mylist.txt'), 
        '-c', 'copy',
        os.path.join(dst, barcode + '.wav')
    ]
    subprocess.call(cmd)

    # deleting temporary input text file
    os.remove(os.path.join(src, barcode, 'mylist.txt'))
    
def is_dvd(src, barcode):
    
    dvd = False
    
    for name in os.listdir(os.path.join(src, barcode)):
        if os.path.splitext(name)[1].startswith('.iso'):
            dvd = True
    
    return dvd
 
def mk_mp4(src, barcode, dst):
 
    for name in os.listdir(os.path.join(src, barcode)):
        if os.path.splitext(name)[1].startswith('.iso'):
            
            # get title count
            cmd = [
                os.path.join('HandBrakeCLI-1.0.7-win-x86_64', 'HandBrakeCLI.exe'),
                '-i', os.path.join(src, barcode, name),
                '-t', '0'
            ]
            # https://www.saltycrane.com/blog/2008/09/how-get-stdout-and-stderr-using-python-subprocess-module/
            p = subprocess.Popen(cmd, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
            output = p.stdout.read()
            
            match = re.findall('scan: DVD has (\d+) title\(s\)', output)
            
            title_count = 1
            if match:
                title_count = int(match[0])

            # make mp4 for barcode
            if title_count == 1:
                print '\nMaking .MP4 for ' + barcode

                cmd = [
                    os.path.join('HandBrakeCLI-1.0.7-win-x86_64', 'HandBrakeCLI.exe'),
                    '-Z', 'High Profile',
                    '-i', os.path.join(src, barcode, name),
                    '-o', os.path.join(dst, os.path.splitext(name)[0] + '.mp4')
                ]
                subprocess.call(cmd)
            
            # make mp4 for each title in barcode
            else:
                count = 1
                while count <= title_count:
                    print '\nMaking .MP4 for title ' + str(count) + ' of ' + str(title_count)
                    
                    cmd = [
                        os.path.join('HandBrakeCLI-1.0.7-win-x86_64', 'HandBrakeCLI.exe'),
                        '--title', str(count),
                        '-Z', 'High Profile',
                        '-i', os.path.join(src, barcode, name),
                        '-o', os.path.join(dst, os.path.splitext(name)[0] + '-' + str(count) + '.mp4')
                    ]
                    subprocess.call(cmd)
                    count += 1


# script
include = ''
if args.include:
    include = args.include

exclude = ''
if args.exclude:
    exclude = args.exclude

include_list = get_include(args.src, include, exclude)

if args.type == 'cd':
    for barcode in include_list:
    
        mk_wav(args.src, barcode, args.dst)

elif args.type == 'dvd':
    for barcode in include_list:
    
        dvd = is_dvd(args.src, barcode)
                
        if dvd == False:
            print 'Not making .MP4s for barcode ' + barcode + '--not a DVD!'
        
        else:
            mk_mp4(args.src, barcode, args.dst)   
        

print "\nAlright, we're done!"
