#!/usr/bin/python
##-------------------------------------------------------------------------
## Description: To generate a file about genes contain infomation as follows:
## chrN start_codon end_codon symbol_of_chain transcript_number
## gene_id gene_name gene_biotype
## te_in_gene: gene_length overlapped_TE_length TE_fraction_in_gene
## te_in_cds: total_length_of_this_gene cds_length_overlapped_TE TE_fraction_in_cds
## disease_gene: -(not in OMIM) 1996(added in OMIM in 1996)
##-------------------------------------------------------------------------
## firstly written by gentle smart hansome dfcao ## 2014/12/15 ##
##--------------------------------------------------------------------------

import os
import sys
from scripts import transcript_num_in_gene,cds_in_gene,sort_features, rm2bed, te_in_gene, te_in_cds, disease_info, filt_duplicate

if (len(sys.argv) < 4):
    print "\npara error! need to use:\npython %s hg19_ensembl73.gtf hg19.rm newDiseaseGeneEachYear\n" % sys.argv[0]
    print "open README.md to read valuable infomation!!!"
    sys.exit()

## get transcript number of each gene
gene_tran_num = os.path.split(sys.argv[1])[1] + ".tranNum"
transcript_num_in_gene.get_tran_num_per_gene(sys.argv[1], gene_tran_num)

## sort annotation of ensembl.tranNum
gene_tran_num = os.path.split(sys.argv[1])[1] + ".tranNum"
sort_features.sort_features(gene_tran_num, 22, 2)
os.system("rm %s" % gene_tran_num)

## get cds regions in each gene
cds_in_gene.get_cds_region(sys.argv[1])

## sort annotation of ensembl.cds
gene_cds = os.path.split(sys.argv[1])[1] + ".cds"
sort_features.sort_features(gene_cds, 22, 2)
os.system("rm %s" % gene_cds)

## transform repeatmasker into bed format
rm2bed.rm2bed(sys.argv[2])
te_in = os.path.split(sys.argv[2])[1] + ".bed.sort"
rm2bed.get_te(te_in)
os.system("rm %s" % (os.path.split(sys.argv[2])[1] + ".bed"))
os.system("rm %s" % te_in)

## reserve one piece of duplicated region in TEs
te_out = os.path.split(sys.argv[2])[1] + ".bed.sort.te"
filt_duplicate.filt_duplicate(te_out)
os.system("rm %s" % te_out)

## calculate fraction of TEs in each gene
gene_tran_num_sort = os.path.split(sys.argv[1])[1] + ".tranNum.sort"
te_uniq = os.path.split(sys.argv[2])[1] + ".bed.sort.te.uniq"
te_in_gene.add_te_in_gene(gene_tran_num_sort, te_uniq)
os.system("rm %s" % gene_tran_num_sort)

## calculate TE fration in cds in each gene
gene_tran_num_sort_tegene = os.path.split(sys.argv[1])[1] + ".tranNum.sort.tegene"
cds_sort = os.path.split(sys.argv[1])[1] + ".cds.sort"
te_uniq = os.path.split(sys.argv[2])[1] + ".bed.sort.te.uniq"
te_in_cds.add_te_in_cds(gene_tran_num_sort_tegene, cds_sort, te_uniq)
os.system("rm %s" % te_uniq)
os.system("rm %s" % cds_sort)
os.system("rm %s" % gene_tran_num_sort_tegene)

## add disease infomation
gene_tran_num_sort_tegene_tecds = os.path.split(sys.argv[1])[1] + ".tranNum.sort.tegene.tecds"
disease_info.disease_info(gene_tran_num_sort_tegene_tecds, sys.argv[3])
os.system("rm %s" % gene_tran_num_sort_tegene_tecds)
gene_tran_num_sort_tegene_tecds_disease = gene_tran_num_sort_tegene_tecds + ".disease"

result = "GeneInfomation.txt"
os.system("mv %s %s" % (gene_tran_num_sort_tegene_tecds_disease, result))
