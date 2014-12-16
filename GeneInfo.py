#!/usr/bin/python
##-------------------------------------------------------------------------
## Description:sort features.
## written by dfcao ## 2014/12/15 ##
##--------------------------------------------------------------------------

import os
import sys
import sort_features
import get_tran_num_per_gene

if (len(sys.argv) < 2):
    print "para error! need to use:\npython %s ensembl-version.gtf\n" % sys.argv[0]
    sys.exit()

## get transcript number of each gene
get_tran_num_per_gene.get_tran_num_per_gene(sys.argv[1])

## sort annotation of ensembl
sort_features.sort_features(sys.argv[1] + ".tranNum", 22, 4)

