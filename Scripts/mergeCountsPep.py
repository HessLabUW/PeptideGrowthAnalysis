###############################################################################
# Gaelen Hess
# 11/07/2022
###############################################################################
# Import neccessary modules

'''
This merges peptide count files to make compatible with analyzeCountsPep.py
'''

from __future__ import division
import csv
import time
import argparse
import pandas as pd
import sys
import os
import numpy as np


###############################################################################    
# Version number

current_version = '1.0'


###############################################################################    

# Parses input using argparse module

# Initiates input parser
parser = argparse.ArgumentParser(description='Merge count files for peptides to make compatible with analyzeCountsPep')

# Non-optional arguments:
parser.add_argument('parameter_file', help='csv file with ID, File Seed, Sample', type=str)

parser.add_argument('output_folder', help='output folder for merged count files', type=str)

# Options for element IDs

# Saves all input to object args
args = parser.parse_args()


###############################################################################
# Process parameter file

FileInfo=pd.read_csv(args.parameter_file, header=0)

for gr_name, sample in FileInfo.groupby('Sample'):
  countfiles=[]
  for row_name, row in sample.iterrows():
    countfile=pd.read_csv(row['FileSeed']+"_counts.csv", header=None, names=['ID', 'Count'])
    countfile.ID=countfile.ID+"__"+row['Name']
    countfiles.append(countfile)
  samplecount=pd.concat(countfiles)
  samplecount.to_csv(os.path.join(args.output_folder,gr_name+"_counts.csv"), header=False, index=False)
  print("Wrote "+os.path.join(args.output_folder,gr_name+"_counts.csv"))
