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

def add_te_in_cds(f_name_gene, f_name_cds, f_name_rm):
    print "\ncalculate TE percentage in cds in each gene...\n"

    re_gene = re.compile('^chr(?P<chr>[\dxXyY]{1,2})\s+(?P<start>\d+)\s+(?P<end>\d+)\s+.*gene_name "(?P<gene_name>[\w\.\-\:]+)";\s+')
    #initial the hash, genes
    genes = {}
    f_gene = open(f_name_gene)
    while True:
        l_now = f_gene.readline()
        if len(l_now) == 0:
            break

        m = re_gene.match(l_now)
        if m == None:
            try:
                print m.groups()
            except:
                print l_now
            print "regular expression match error!\n"
            sys.exit()

        genes[m.group("gene_name")] = [0, 0]#[cds_bp, cds_overlap_te_bp]
    f_gene.close

    #initial hash tes, tes[chr] = [start, end]
    f_rm = open(f_name_rm)
    tes = {}
    for chr_i in range(1, 25):
        tes[chr_i] = []

    #store TE infomation in the vector tes
    re_bed = re.compile('^chr(?P<chr>[\dxXyY]{1,2})\s+(?P<start>\d+)\s+(?P<end>\d+)')
    while True:
        l_now = f_rm.readline()
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

        tes[chrom2num(m.group("chr"))].append([string.atoi(m.group("start")), string.atoi(m.group("end"))])
    f_rm.close

    #calculate TE fraction in cds in each gene
    f_cds = open(f_name_cds)
    last_chr = 0
    te_chr = 1 #index of tes, range:1-24
    i = 0 #index of tes[chr] 
    while True:
        l_now = f_cds.readline()
        #print l_now

        if len(l_now) == 0:
            break
        if te_chr == 25:
            continue

        m = re_gene.match(l_now)
        if m == None:
            print "regular expression match error!\n"
            sys.exit()

        chrome = chrom2num(m.group("chr"))
        start = string.atoi(m.group("start"))
        end = string.atoi(m.group("end"))
        gene_name = m.group("gene_name")

        if last_chr != chrome:
            print "chr%s is in processing..." % chrome
        last_chr = chrome

        if te_chr < 25 and i == len(tes[te_chr]):
            te_chr += 1
            i = 0

        if te_chr < 25 and chrome != te_chr:
            if chrome > te_chr:
                te_chr += 1
                i = 0
            else:
                continue

        if te_chr == 25:
            continue

        #locate the right TE which is in front of the gene
        while i > 0 and start < tes[te_chr][i][1]:
            i -= 1

        #calculate a gene by moving TE vector
        overlap = 0    
        while i < len(tes[te_chr]) and end >= tes[te_chr][i][0]:
            #print "chrte = %d, i = %d, gene_st = %s, gene_en = %s, te_start = %s" % (te_chr, i, start, end, tes[te_chr][i][0])
            while i < len(tes[te_chr]) and chrome == te_chr and start > tes[te_chr][i][1]:
                i += 1
            if i == len(tes[te_chr]) or chrome != te_chr:
                break
            if tes[te_chr][i][0] <= start and start <= tes[te_chr][i][1]:
                if tes[te_chr][i][1] <= end:
                    overlap += (tes[te_chr][i][1] - start + 1)
                    i += 1
                elif end < tes[te_chr][i][1]:
                    overlap += (end - start + 1)
                    break
            elif start < tes[te_chr][i][0] and tes[te_chr][i][0] <= end:
                if tes[te_chr][i][1] <= end:
                    overlap += (tes[te_chr][i][1] - tes[te_chr][i][0] + 1)
                    i += 1
                elif end < tes[te_chr][i][1]:
                    overlap += (end - tes[te_chr][i][0] + 1)
                    break

        genes[gene_name][0] += (end - start + 1)
        genes[gene_name][1] += overlap

    #calculate fraction of TE in cds in each gene
    f_name_out = os.path.split(f_name_gene)[1] + ".tecds"
    f_out = open(f_name_out, 'w')
    f_gene = open(f_name_gene)
    while True:
        l_now = f_gene.readline()
        if len(l_now) == 0:
            break

        m = re_gene.match(l_now)
        if m == None:
            print "regular expression match error!\n"
            sys.exit()

        fraction = 0
        if genes[m.group("gene_name")][0] > 0:
            fraction = float(genes[m.group("gene_name")][1]) * 100/ genes[m.group("gene_name")][0]
        #print fraction
        l_out = "%s\tte_in_cds %d %d %.2f\n" % (l_now.strip(), genes[m.group("gene_name")][0], genes[m.group("gene_name")][1], fraction)
        f_out.write(l_out)
    f_gene.close
    f_out.close


#---------------------------------------------------------------
# test
# if (len(sys.argv) < 4):
#     print "para error! need to use:\npython %s ensembl73.gtf.tranNum.sort.tegene ensembl73.gtf.cds.sort human19.rm.bed.sort.te.uniq\n" % os.path.split(sys.argv[0])[1]
#     sys.exit()

# add_te_in_cds(sys.argv[1], sys.argv[2], sys.argv[3])
