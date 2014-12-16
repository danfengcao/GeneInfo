#!/usr/bin/python
##-------------------------------------------------------------------------
## Description:get information of transcript number per gene.
## written by dfcao ## 2014/12/15 ##
##--------------------------------------------------------------------------

import re
import sys
import os
import string
import sort_features

if (len(sys.argv) < 2):
    print "para error! need to use:\npython %s ensembl73.gtf\n" % sys.argv[0]
    sys.exit()

#----------------------------------------------------------------
# output info of a gene into the f_out
# f_out: output file
# gene:  an array stores all infomation of a gene in ensembl gtf format
def output_gene(f_out, gene):
    re_ensembl_gtf = re.compile('^(?P<chr>[\dxXyY]{,2})\s+\w+\s+\w+\s+(?P<start>\d+)\s+(?P<end>\d+)\s+\.\s+(?P<symbol>[+-])\s+\.\s+gene_id "(?P<gene_id>[\w\-\.]+)"; transcript_id "(?P<tran_id>[\w\-\.\:]+)";.*gene_name "(?P<gene_name>[\w\-\.\:]+)"; gene_biotype "(?P<gene_biotype>[\w\-\.]+)"')
    start = []
    end = []
    tran_id = []
    chrom = ""
    gene_name = ""
    gene_id = ""
    for line in gene:
        m = re_ensembl_gtf.match(line)
        if m == None:
            return
        start.append(string.atoi(m.group("start")))
        end.append(string.atoi(m.group("end")))
        tran_id.append(m.group("tran_id"))
        chrom = m.group("chr")
        gene_name = m.group("gene_name")
        gene_id = m.group("gene_id")
        gene_biotype = m.group("gene_biotype")
        symbol = m.group("symbol")
    
    l_out = 'chr%s\t%d\t%d\t%s\t%d\tgene_id "%s"; gene_name "%s"; gene_biotype "%s"\n' % (chrom, min(start), max(end), symbol, len(list(set(tran_id))), gene_id, gene_name, gene_biotype)
    f_out.write(l_out)

f_ensembl = file(sys.argv[1], 'r')
f_out_name = "tran_num_per_gene." + os.path.split(sys.argv[1])[1]
f_out = file(f_out_name, 'w')

gene_num = 0 #count total number of gene in emsembl gtf file
tran_num = 0 #count total number of transcript in emsembl gtf file
gene_now = [] #store the processing gene

last_gene_id = ""
last_chr = 0
re_gene_id = re.compile('^(?P<chr>[\dxXyY]{1,2})\s+.*gene_id "(?P<gene_id>[\w\-\.]+)";')
while True:
    l_now = f_ensembl.readline()
    if len(l_now) == 0:
        break
        
    m = re_gene_id.match(l_now)
    if m == None:
        continue
    if last_chr != m.group("chr"):
        print "chr%s is in processing" % m.group("chr")
    
    if last_gene_id != m.group("gene_id"):
        #input a new gene now, output the info of last gene
        if gene_num != 0:
            output_gene(f_out, gene_now)
            gene_now = []
        gene_num += 1

    gene_now.append(l_now)
    last_gene_id = m.group("gene_id")
    last_chr = m.group("chr")

print "gene number: %d\n" % gene_num

f_ensembl.close()
f_out.close()

sort_features.sort_features(f_out_name, 22)
