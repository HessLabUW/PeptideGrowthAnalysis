# Written by Gaelen Hess
# Last updated 20200526
#
#
#

import argparse
import pandas as pd
from statsmodels.sandbox.stats.multicomp import multipletests
import os
import csv
import time

version=0.1

parser = argparse.ArgumentParser(description='Generates FDR based on results files')

parser.add_argument('res_file', help='Result file to be treated', type=str)
parser.add_argument('col_name', help='Name of column with pvalues', type=str)
parser.add_argument('cor_method', help='Correction method (Options: bonferroni, sidak, holm-sidak, holm, simes-hochberg, hommel, fdr_bh, fdr_by, fdr_tsbh, fdr_tsbky)' , type=str)

args=parser.parse_args()

name = args.res_file[: -4]
rec_file = name + '_record.txt'

result_info=pd.read_csv(args.res_file, header=0)

#print(result_info)

result_info[args.col_name+' FDR ('+args.cor_method+')']=multipletests(result_info[args.col_name], method=args.cor_method)[1]

result_info.to_csv(name+"_fdr.csv", header=True, index=False)

###############################################################################
# Appends note to existing record

#with open(rec_file, 'a') as rec_open:
#    rec_csv = csv.writer(rec_open, delimiter='\t')
#    rec_csv.writerow(['addFDR.py', version])
#    rec_csv.writerow(['Date', time.strftime("%d:%m:%Y")])
#    rec_csv.writerow(['p-value Column', args.col_name])
#    rec_csv.writerow(['Correction_Method', args.cor_method])
