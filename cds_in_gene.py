#!/usr/bin/python
##-------------------------------------------------------------------------
## Description:get cds region in ensembl database.
## firstly written by adorable charming attractive dfcao ## 2014/12/18 ##
##--------------------------------------------------------------------------

import re
import sys
import os

#----------------------------------------------------------------
# output cds in ensembl database
def get_cds_region(file_name):
    print "\nget cds region in ensembl...\n"

    f_ensembl = open(file_name, 'r')
    f_out_name = os.path.split(file_name)[1] + ".cds"
    f_out = open(f_out_name, 'w')

    re_cds = re.compile('^(?P<chr>[\w\.\:\-]+)\s+\w+\s+CDS\s+(?P<start>\d+)\s+(?P<end>\d+)\s+[\.\d]\s+(?P<symbol>[+-])\s+[\.\d]\s+gene_id "(?P<gene_id>[\w\-\.\:]+)";.*transcript_id "(?P<tran_id>[\w\-\.\:]+)";.*gene_name "(?P<gene_name>[\w\-\.\:]+)";.*gene_biotype "(?P<gene_biotype>[\w\-\.]+)"')
    while True:
        l_now = f_ensembl.readline()
        if len(l_now) == 0:
            break
        
        m = re_cds.match(l_now)
        if m == None:
            continue
        l_out = 'chr%s\t%s\t%s\t%s\tgene_id "%s"; transcript_id "%s" gene_name "%s"; gene_biotype "%s"\n' % (m.group("chr"), m.group("start"), m.group("end"), m.group("symbol"), m.group("gene_id"), m.group("tran_id"), m.group("gene_name"), m.group("gene_biotype"))
        f_out.write(l_out)

    f_ensembl.close()
    f_out.close()


#---------------------------------------------------------------
# test
# if (len(sys.argv) < 2):
#     print "para error! need to use:\npython %s ensembl.gtf\n" % os.path.split(sys.argv[0])[1]
#     sys.exit()

# get_cds_region(sys.argv[1])
