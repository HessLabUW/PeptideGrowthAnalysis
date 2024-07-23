# PeptideGrowthAnalysis

Analysis of proliferation screen for peptide libraries

# Dependencies

Installation of bowtie is required for alignment of the protein domains.

The scripts use python3.7

# Clone Git

'git clone https://github.com/HessLabUW/PeptideGrowthAnalysis'

# Create index for library

# Align Reads and Make Count Files

# Combine Replicates

# Use casTLE

# Calculate p-values and FDR



#### addFDR.py
usage: addFDRPep.py [-h] res_file col_name cor_method

Generates FDR based on results files

###### positional arguments:
  >*res_file*    Result file to be treated\
  >*col_name*    Name of column with pvalues\
  >*cor_method*  Correction method (Options: bonferroni, sidak, holm-sidak, holm, simes-hochberg, hommel, fdr_bh, fdr_by, fdr_tsbh, fdr_tsbky)

###### optional arguments:
  >*-h, --help*  show this help message and exit

###### Output
This generates an additional column in the result file called "castle p-value FDR".  Once you have this, you can select a FDR.  As an example, let's say you select 10% FDR (10% of your hits are false). Anything with an adjusted p-value <0.10 is a hit. If you decide on a 5% FDR, everyting with an adjusted p-value <0.05 would be a hit.