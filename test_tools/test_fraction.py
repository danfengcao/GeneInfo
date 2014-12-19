#!/usr/bin/python 
##-------------------------------------------------------------------------
## Description:sort features.
## firstly written by dfcao ## 2014/12/15 ##
##--------------------------------------------------------------------------

import os
import sys
import re
import string

#----------------------------------------------------------------
# generate test data
def test_te_fraction_in_gene(f_name):
    f_in = open(f_name)
    
    re_fraction = re.compile('^\w+\s+(?P<start>\d+)\s+(?P<end>\d+)\s+(?P<fraction>[\d\.]+)')
    gene_len = 0
    overlap_len = 0
    while True:
        l_now = f_in.readline()
        if len(l_now) == 0:
            break
        
        m = re_fraction.match(l_now)
        start = string.atoi(m.group("start"))
        end = string.atoi(m.group("end"))
        fraction = string.atof(m.group("fraction"))
        
        gene_len += (end - start + 1)
        overlap_len += (end - start + 1) * fraction / 100

    print "fraction = %.2f" % (overlap_len / float(gene_len))
        
def test_te_fraction_in_cds(f_name):
    f_in = open(f_name)
    
    re_fraction = re.compile('^\w+\s+(?P<cds>\d+)\s+(?P<overlap>[\d\.]+)\s+')
    cds_len = 0
    overlap_len = 0
    while True:
        l_now = f_in.readline()
        if len(l_now) == 0:
            break
        
        m = re_fraction.match(l_now)
        cds = string.atoi(m.group("cds"))
        overlap = string.atoi(m.group("overlap"))
        
        cds_len += cds
        overlap_len += overlap

    print "cds_len = %d, fraction = %.2f" % (cds_len, overlap_len * 100/ float(cds_len))
    

#---------------------------------------------------------------
# test
if (len(sys.argv) < 2):
    print "para error! need to use:\npython %s te.fraction" % sys.argv[0]
    sys.exit()

#test_te_fraction_in_gene(sys.argv[1])
test_te_fraction_in_cds(sys.argv[1])
