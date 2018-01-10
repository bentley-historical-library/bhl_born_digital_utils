# bhl_ripstation_utils
RipStation scripts used by the Bentley Historical Library

**Table of Contents**
  * [mk-dips](https://github.com/bentley-historical-library/bhl_ripstation_utils#mk-dir)

## mk-dips
usage: mk-dips.py [-h] --type {data,cd,dvd} --src SRC --dst DST

Make DIPs from the RipStation (AKA Jackie).

optional arguments:

| Argument | Help |
| --- | --- |
| -h, --help | show this help message and exit |
| --type {data,cd,dvd} | Pick one: Data CD(s) or DVD(s); audio CD(s); or video-formatted DVD(s) |
| --src SRC | Input directory |
| --dst DST | Output directory |
