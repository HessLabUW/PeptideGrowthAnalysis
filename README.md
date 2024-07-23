# PeptideGrowthAnalysis

Analysis of proliferation screen for peptide libraries

# Dependencies

Installation of bowtie is required for alignment of the protein domains.

The scripts use python3.7

# Clone Git

'git clone https://github.com/HessLabUW/PeptideGrowthAnalysis'

# Step 1: Create index for library
*This step requires bowtie to be installed*

If you have generated an index for this library previously, you don't have to recreate it.  Using "python /PATH_TO_SCRIPTS/makeCounts.py -h" will show a list of previously made libraries. You can also open the screen_type_index.txt file in the Indices folder to see the list.

The oligo_file is a .csv file that contains a sgRNA_ID in the first column and the sequence of the oligo ordered from a chip. These are often located in the /project6/HessLabCHGPM/OligoChips/ folder.  Given it encodes the full oligo, it includes other parts of the sequence that are not part of the sgRNA sequence that you don't want to include for the alignment. Therefore, we trim off all of these parts from the oligo in this script so we make an alignment that is just the sgRNA sequence.

#### makeIndices.py
>usage: Make index for alignment [-h] [-s STRIM] [-e ETRIM] [-n NUMS] [-o] [-t] [-b BOWTIE] oligo_file short_name full_name

###### positional arguments:
  >*oligo_file*            Input oligo file; csv format\
  >*short_name*            The screen type for reference\
  >*full_name*             Name for output files

###### optional arguments:
  >*-h, --help*            show this help message and exit\
  >*-s STRIM, --strim STRIM*
                        Trim bases from start; default is 0\
  >*-e ETRIM, --etrim ETRIM*
                        Trim bases from end; default is 0\
  >*-n NUMS, --nums NUMS*  Number of oligos to output (Default is 2)\
  >*-o, --override*        Flag to override existing indexes\
  >*-t, --test*            Flag to not run bowtie \
  >*-b BOWTIE, --bowtie BOWTIE*
                        Location of Bowtie aligner; default is home drive

Run this script first without the *-t* flag and it will show you what the actual sequences you are using to build the indice..  You can then determine the porper trims using the *-s* and *-e* flags.  Once you are sure you have the right oligos.  Run with the *-t* flag which will generate the bowtie index files in the Indices folder as well as update the screen_type_index.txt

###### Output:

This generates the bowtie files in the Indices folder and updates the screen_type_index.txt in the Indices folder as well.

# Step 2: Align Reads and Make Count Files

*This step requires bowtie*

#### makeCounts.py
>usage: makeCounts.py [-h] [-m MISMATCH] [-l READ_LENGTH] [-fi] [-b BOWTIE] [-a ADD_FILE] [-s {-,+}] [-p PROCESS]
                     file_in name
                     {List of Library names}

###### positional arguments:

  >*file_in*               File base for input fastq files (it has to be a root so, it can't contain the .fastq.gz part of the name)\
  >*name*                  Name for output files\
  >*{List of Library names}*
                        The screen type: The List of Library names will tell you which of the indices you can use for alignment.

###### optional arguments:

  >*-h, --help*            show this help message and exit\
  >*-m MISMATCH, --mismatch MISMATCH*
                        The number of tolerated mismatches; default is 0\
  >*-l READ_LENGTH, --length READ_LENGTH*
                        Select the number of bases to align; default is 17\
  >*-fi, --filter*         Flag to filter too short reads\
  >*-b BOWTIE, --bowtie BOWTIE*
                        Location of Bowtie aligner; default is bowtie\
  >*-a ADD_FILE, --add_file ADD_FILE*
                        Location of additional FASTQ files, if any\
  >*-s {-,+}, --strand {-,+}*
                        Filters reads by alignment strand; default is none\
  >*-p PROCESS, --process PROCESS*
                        Number of processors to use; default is 8

The defaults are okay for most processes. I run with "-m 0" unless the run had poor sequencing quality. For the CRKO library, I would use the default of "-l 17". For CRISPR-X libraries, I would use "-l 20" the full length of the sgRNA. For CRISPRi/a from the Weissman lab, I would use "-l 19".

###### Output:

For each fastq file, you will generate a _counts.csv file which lists each sgRNA and the number of counts detected. sgRNAs not detected will simply not be listed in this file.


# Combine Replicates

# Use casTLE

#### analyzeCounts.py
>usage: analyzeCounts.py [-h] [-n NEG_NAME] [-s SPLIT_MARK] [-x EXCLUDE [EXCLUDE ...]] [-t THRESH] [-k K]
                        [-b {all,neg,tar}] [-z ZERO_FILES ZERO_FILES] [-c SCALE] [-I I_STEP] [-p NUMS] [-r REFERENCE]
                        [-of] [-m] [-ro]
                        unt_file trt_file name

Compares count files using casTLE

###### positional arguments:
  >*unt_file*              File for untreated counts\
  >*trt_file*              File for treated counts\
  >*name*                  Name for output files

###### optional arguments:
  >*-h, --help*            show this help message and exit\
  >*-n NEG_NAME, --neg_name NEG_NAME*
                        Symbol used to denote negative controls. Default is 0.\
  >*-s SPLIT_MARK, --split SPLIT_MARK*
                        Delimiter for element name. Default is _\
  >*-x EXCLUDE [EXCLUDE ...], --exclude EXCLUDE [EXCLUDE ...]*
                        Only include elements containing substrings.\
  >*-t THRESH, --threshhold THRESH*
                        Read cutoff for small count numbers. Default is 10.\
  >*-k K, --strength K*    Normalizing constant. Default is 1.\
  >*-b {all,neg,tar}, --back {all,neg,tar}*
                        Background population for noise estimation. Default is neg.\
  >*-z ZERO_FILES ZERO_FILES, --zero_files ZERO_FILES ZERO_FILES*
                        Time zero count files. Optional.\
  >*-c SCALE, --scale SCALE*
                        Scale of calculations; default is 3\
  >*-I I_STEP, --I_step I_STEP*
                        Step size in grid search; default is 0.1\
  >*-p NUMS, --proccessors NUMS*
                        Number of proccessors to use; default is 20\
  >*-r REFERENCE, --reference REFERENCE*
                        Location of reference files; default is GeneRef\
  >*-of, --override_file*  Overrides restriction of output to Results folder\
  >*-m, --mouse*           Uses mouse gene information.\
  >*-ro, --record*         Allows script to run without record of count files.
  
###### Output

For each comparison, it will generate a csv file (referred to as a result file) with the following columns:
1. #GeneID - HGNC ID number
2. Symbol - HGNC Symbol
3. GeneInfo - Full Name
4. Localization - GO Term Localization
5. Process - GO Term Process
6. Function - GO Term Function
7. Element # - # of sgRNAs detected
8. casTLE Effect - Effect of gene perturbation (roughly think of as a predicted Log2 Fold Change)
9. casTLE Score - Statistical score for significance of effect
10. casTLE p-value - will be N/A for this, but will be filled in later
11. Minimum Effect Estimate - Minimum Effect size in 95% confidence interval
12. Maximum Effect Estimate - Maximum Effect size in 95% confidence interval
13. Individual Elements (List of individual sgRNAs and their effect sizes)


# Calculate p-values and FDR
There are two versions for this.  addPermutations.py is for a single replicate and addCombo.py is for two combined replicates. I generally don't run addPermutations if I am going to analyze it as combined replicates.

A common question is "how many permutations should I run?" As a rule of thumb, you should run 20 * Number of genes/elements)). For example, for a genome wide screen of 20,000 genes, you should run approximately 400,000 permutations. The way this script works is that it picks a number of genes and calcualtes a castle score for this random "gene". It saves this score in a _ref.csv file. Therefore, if you came back later to do more permutations, you can add onto the ones you already have previously performed. 

#### addPermutations.py
usage: addPermutations.py [-h] [-p NUMS] [-e] [-t] [-r RATIO_COL] [-m] res_file perm_num

Adds permutations for p-values

###### positional arguments:
  >*res_file*              Results file\
  >*perm_num*              Number of permutations

###### options:
  >*-h, --help*            show this help message and exit\
  >*-p NUMS, --proccessors NUMS*
                        Number of prcessors to use\
  >*-e, --erase*           Erase previous permutations\
  >*-t, --out_time*        Output timestamps.\
  >*-r RATIO_COL, --ratio_col RATIO_COL*
                        Column containing ratio scores\
  >*-m, --mouse*           Uses mouse gene information.

###### Output

This will fill in the "casTLE p-value" column in the combo result file.  It will also generate the _ref.csv file that contains the casTLE scores for all of the permutations.


#### addFDRPep.py
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