#!/usr/bin/python2.7
'''
get information of transcript number per gene.

firstly written by compassionate aggressive glamorous dfcao, 2014/12/15
'''

__author__ = 'dfcao'

import sys
import os
import re
import string

def output_gene(f_out, gene):
    '''Output information of a gene into the file f_out

    f_out: FILE operator of output file
    gene: an array stores all infomation of a gene in ensembl gtf format'''

    re_ensembl_gtf = re.compile('^(?P<chr>[\w\.\:\-]+)\s+\w+\s+\w+\s+(?P<start>\d+)\s+(?P<end>\d+)\s+[\.\d]\s+(?P<symbol>[+-])\s+[\.\d]\s+gene_id "(?P<gene_id>[\w\-\.\:]+)"; transcript_id "(?P<tran_id>[\w\-\.\:]+)";.*gene_name "(?P<gene_name>[\w\-\.\:]+)"; gene_biotype "(?P<gene_biotype>[\w\-\.]+)"')
    start = []
    end = []
    tran_id = []
    chrom = ""
    gene_name = ""
    gene_id = ""

    #print gene
    for line in gene:
        m = re_ensembl_gtf.match(line)
        if not m:
            print line
            print '^(?P<chr>[\w\.\:\-]+)\s+\w+\s+\w+\s+(?P<start>\d+)\s+(?P<end>\d+)\s+[\.\d]\s+(?P<symbol>[+-])\s+[\.\d]\s+gene_id "(?P<gene_id>[\w\-\.\:]+)";transcript_id "(?P<tran_id>[\w\-\.\:]+)";.*gene_name "(?P<gene_name>[\w\-\.\:]+)"; gene_biotype "(?P<gene_biotype>[\w\-\.]+)"'
            print "here regular expression error!"
            sys.exit()

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


def get_tran_num_per_gene(f_name_gtf, f_name_out = ""):
    '''Get transcript number per gene in ensembl.

    f_name_gtf: name of gtf format file, such as ensembl.gtf
    f_name_out: name of output file'''

    print "get transcript number per gene in ensembl..."

    f_ensembl = open(f_name_gtf, 'r')
    if f_name_out == "":
        f_name_out = os.path.split(f_name_gtf)[1] + ".tranNum"
    f_out = open(f_name_out, 'w')

    gene_num = 0 #count total number of gene in emsembl gtf file
    tran_num = 0 #count total number of transcript in emsembl gtf file
    gene_now = [] #store the processing gene

    last_gene_id = ""
    last_chr = 0
    re_gene_id = re.compile('^(?P<chr>[\w\.\:\-]+)\s+.*gene_id "(?P<gene_id>[\w\-\.\:]+)";')
    while True:
        l_now = f_ensembl.readline()
        if not l_now:
            break
        if re.match('^#', l_now):
            continue

        m = re_gene_id.match(l_now)
        if not m:
            try:
                print m.groups()
            except:
                print l_now
            print "regular expression error!\n"
            sys.exit()

        if last_chr != m.group("chr"):
            print "chr%s is in processing..." % m.group("chr")
    
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


#---------------------------------------------------------------
# test
if __name__ == '__main__':
    if (len(sys.argv) < 3):
        print "Para error! need to use:\npython %s ensembl73.gtf output_file_name" % os.path.split(sys.argv[0])[1]
        sys.exit()

    get_tran_num_per_gene(sys.argv[1], sys.argv[2])
