#!/usr/bin/python 
##-------------------------------------------------------------------------
## Description:sort features.
## written by dfcao ## 2014/12/15 ##
##--------------------------------------------------------------------------

import os
import sys

#----------------------------------------------------------------
# sort a gtf or bed format file by its first two feartures
# chromosome and start codon in this script
# f_name: input file to be processed
# nonsex_chrs: the number of nonsex chromosomes
def sort_features(f_name, nonsex_chrs):
    f_in = file(f_name)
    f_out = os.path.split(f_name)[1] + ".sort"

    parts = ""
    chr_list = range(1, nonsex_chrs+1)
    chr_list.append('X')
    chr_list.append('Y')
    for i in chr_list:
        print "sorting chr%s..." % i
        tmp_file = "file" + str(hash(f_name + str(i)))
        os.system("grep -P 'chr%s\t' %s | sort -n -k 2  >%s" % (str(i), f_name, tmp_file))
        parts += (tmp_file + " ")
        
    os.system("cat " + parts + ">" + f_out)

    for i in chr_list:
        tmp_file = "file" + str(hash(f_name + str(i)))
        os.system("rm " + tmp_file)
#---------------------------------------------------------------
# unit test
# if (len(sys.argv) < 2):
#     print "para error! need to use:\npython %s ensembl.gtf\n" % sys.argv[0]
#     sys.exit()

# sort_features(os.path.split(sys.argv[1])[1], 22)
