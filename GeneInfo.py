#!/usr/bin/python
##-------------------------------------------------------------------------
## Description: To generate a file about genes contain infomation as follows:
## chrN start_codon end_codon symbol transcript_number_in_this_gene gene_id
##-------------------------------------------------------------------------
## firstly written by gentle smart hansome dfcao ## 2014/12/15 ##
##--------------------------------------------------------------------------

import os
import sys
import sort_features
import get_tran_num_per_gene
import rm2bed
import te_percentage_in_each_gene
import disease_info

if (len(sys.argv) < 4):
    print "para error! need to use:\npython %s ensembl-version.gtf human19.rm newDiseaseGeneYear\n" % sys.argv[0]
    sys.exit()

## get transcript number of each gene
#get_tran_num_per_gene.get_tran_num_per_gene(sys.argv[1])

## sort annotation of ensembl
#gene_tran_num = sys.argv[1] + ".tranNum"
#sort_features.sort_features(gene_tran_num, 22, 2)

## transform repeatmasker into bed format
#rm2bed.rm2bed(sys.argv[2])
#te_in = sys.argv[2] + ".bed.sort"
#rm2bed.get_te(te_in)

## calculate fraction of TEs in each gene
# gene_tran_num_sort = sys.argv[1] + ".tranNum.sort"
# te_out = sys.argv[2] + ".bed.sort.te"
# te_percentage_in_each_gene.te_percentage(gene_tran_num_sort, te_out)

## add disease infomation
ensem_te_fraction = sys.argv[1] + ".tranNum.sort.fraction"
disease_info.disease_info(ensem_te_fraction, sys.argv[3])
