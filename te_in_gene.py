#!/usr/bin/python
##---------------------------------------------------------------------
## Description:
## calculate fraction of te in each genes.
##---------------------------------------------------------------------
## firstly written by selfless sporting adorable dfcao. ## 2014/12/17 
##********************************************************************* 

import re
import sys
import os
import string

def chrom2num(chrome):
    if cmp(chrome, 'X') == 0 or cmp(chrome, 'x') == 0:
        return 23
    elif cmp(chrome, 'Y') == 0 or cmp(chrome, 'y') == 0:
        return 24
    else:
        return string.atoi(chrome)

def add_te_in_gene(f_name_gene, f_name_rm):
    print "calculate te percentage of te in each gene..."
    f_out_name = os.path.split(f_name_gene)[1] + ".fraction"
    f_out = open(f_out_name, 'w')
    f_tmp_name = "file" + str(hash(f_name_gene))
    
    print "use bedtools to get intersect region..."
    os.system("bedtools intersect -a " + f_name_gene + " -b " + f_name_rm + " > " + f_tmp_name)
    
    genes = {}
    f_gene = open(f_name_gene)
    f_tmp = open(f_tmp_name)
    re_bed = re.compile('^chr(?P<chr>[\dxXyY]{1,2})\s+(?P<start>\d+)\s+(?P<end>\d+)\s+.*gene_id "(?P<gene_id>[\w\.\-\:]+)";\s+')
    
    #store ensembl gene_id in the hash genes
    while True:
        l_now = f_gene.readline()
        if len(l_now) == 0:
            break

        m = re_bed.match(l_now)
        if m == None:
            try:
                print m.groups()
            except:
                print l_now
            print "regular expression match error!\n"
            sys.exit()

        genes[m.group("gene_id")] = [string.atoi(m.group("start")), string.atoi(m.group("end")), 0]
    f_gene.close

    #traverse overlapped region
    while True:
        l_now = f_tmp.readline()
        if len(l_now) == 0:
            break

        m = re_bed.match(l_now)
        if m == None:
            print "regular expression match error!\n"
            sys.exit()

        genes[m.group("gene_id")][2] += (string.atoi(m.group("end")) - string.atoi(m.group("start")) + 1)
    f_tmp.close

    #calculate fraction of TE in each gene
    f_gene = open(f_name_gene)
    while True:
        l_now = f_gene.readline()
        if len(l_now) == 0:
            break

        m = re_bed.match(l_now)
        if m == None:
            print "regular expression match error!\n"
            sys.exit()

        fraction = float(genes[m.group("gene_id")][2]) * 100/ (genes[m.group("gene_id")][1] - genes[m.group("gene_id")][0] + 1)
        l_out = "%s\tte_in_gene %.2f\n" % (l_now.strip(), fraction)
        f_out.write(l_out)
    f_gene.close
    f_out.close


#---------------------------------------------------------------
# test
# if (len(sys.argv) < 3):
#     print "para error! need to use:\npython %s ensembl.gtf.tranNum.sort human19.rm.bed.sort.te\n" % os.path.split(sys.argv[0])[1]
#     sys.exit()

# add_te_in_gene(sys.argv[1], sys.argv[2])
