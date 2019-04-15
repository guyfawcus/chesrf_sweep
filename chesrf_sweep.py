#!/usr/bin/env python3

import argparse
import csv
import io
import shutil
import subprocess
import sys

# Parse Arguments
parser = argparse.ArgumentParser(description='Wireless Workbench scan generator that uses hackrf_sweep')
parser.add_argument('-o', '--output', default='./output.csv', metavar='FILE', help='Output file')
parser.add_argument('-b', '--bottom', default=400, type=int, metavar='Hz', help='Bottom end frequency bound')
parser.add_argument('-t', '--top', default=800, type=int, metavar='Hz', help='Top end frequency bound')
parser.add_argument('-w', '--width', default=2500, type=int, metavar='Hz', help='Sample bin width')
parser.add_argument('-z', '--offset', default=-23000, type=int, metavar='Hz', help='Frequency offset')
parser.add_argument('-g', '--gain', default=-30, type=int, metavar='dB', help='Gain adjust')
args = parser.parse_args()

# Check if the hackrf_sweep command is avaliable
if shutil.which('hackrf_sweep') is None:
    print('The "hackrf_sweep" command is not avaliable!')
    print('Please follow this guide to install the HackRF tools then try again:')
    print('https://github.com/mossmann/hackrf/wiki/Operating-System-Tips')
    sys.exit(1)

# Build command
command_str = ['hackrf_sweep', '-1',
               '-f', '{}:{}'.format(args.bottom, args.top),
               '-w', '{}'.format(args.width)]

# Run command and return output if there was a problem
print('Running command: {}'.format(' '.join(command_str)))
command = subprocess.run(command_str, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

if command.returncode != 0:
    print('\n' + command.stderr.decode().strip())
    sys.exit(1)

# Read in the output from the command directly
print('Reading output')
csvreader = csv.reader(io.StringIO(command.stdout.decode()), delimiter=',', skipinitialspace=True)

# Loop over the results and do the do
print('Offsetting results by {} Hz'.format(args.offset))
print('Adjusting gain by {}{} dB'.format(('+' if args.gain > 0 else ''), args.gain))
freqs = []
powers = []
for line in csvreader:
    date = line[0]
    time = line[1]
    hz_low = int(line[2])
    hz_high = int(line[3])
    hz_bin_width = float(line[4])
    num_samples = line[5]

    for number, value in enumerate(line[6:], start=1):
        # Calculate the frequency for each bin and convert to MHz
        freq = ((hz_low + (hz_bin_width * number) - (hz_bin_width / 2)) + args.offset) / 1000000
        freqs.append('{:.3f}'.format(freq))
        powers.append(float(value) + args.gain)

results = list(zip(freqs, powers))

# Save the output
print('Saving output to {}'.format(args.output))
with open(args.output, 'w') as csvfile:
    csvwriter = csv.writer(csvfile)
    for result in results:
        csvwriter.writerow(result)
