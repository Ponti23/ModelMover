# -*- coding: utf-8 -*-
"""
Created on Fri Oct 18 15:12:27 2024

@author: Charlie
"""
import os

input_file = 'SpaceBox002.obj'  # Change this to your input file name
output_file = input_file.strip('.obj') + "_scaled.obj"

with open(input_file, 'r') as f:
    lines = f.readlines()

with open(output_file, 'w') as f:
    for line in lines:
        if line.startswith('v '):
            parts = line.split()
            # Assuming the first part is 'v', and the rest are the numbers
            new_line = f"{parts[0]} "
            new_numbers = [str(float(num) / 100) for num in parts[1:]]
            new_line += ' '.join(new_numbers) + '\n'
            f.write(new_line)
        else:
            f.write(line)  # Write unchanged lines to the output file

# Delete the original file
os.remove(input_file)
os.rename(output_file, input_file)