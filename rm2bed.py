#!/usr/bin/python
##-------------------------------------------------------------------------
## Description:transform raw data of repeatmasker into bed format.
## firstly written by dfcao ## 2014/12/17 ##
##--------------------------------------------------------------------------

import re
import sys
import os
import sort_features

def rm2bed(rm_file):
    print "\ntransform repeatmasker file into bed format...\n"

    f_rm = open(rm_file, 'r')
    f_out_name = os.path.split(rm_file)[1] + ".bed"
    f_out = open(f_out_name, 'w')

    last_chr = 0
    re_rm_repeat = re.compile('^[\d\s]+.*chr(?P<chr>[\dxXyY]{1,2})\s+(?P<start>\d+)\s+(?P<end>\d+)\s+[\(\)\w]+\s+[\w\+]\s+[\(\)\w\-\?]+\s+(?P<r_class>[\w\-\/\?]+)\s+')
    while True:
        l_now = f_rm.readline()
        if len(l_now) == 0:
            break
        
        m = re_rm_repeat.match(l_now)
        if m == None:
            continue

        chrom = m.group("chr")
        start = m.group("start")
        end = m.group("end")
        r_class = m.group("r_class")
        if last_chr != chrom:
            print "chr%s is in processing..." % chrom
            
        l_out = 'chr%s\t%s\t%s\t%s\n' % (chrom, start, end, r_class)
        f_out.write(l_out)
        last_chr = chrom

    f_rm.close
    f_out.close
    sort_features.sort_features(f_out_name, 22, 2)

def get_te(rm_sort_file):
    print "get TE elements in repeatmasker...\n"
    
    f_rm = open(rm_sort_file, 'r')
    f_out_name = os.path.split(rm_sort_file)[1] + ".te"
    f_out = open(f_out_name, 'w')

    last_chr = 0
    re_rm_repeat = re.compile('^\w+\s+\d+\s+\d+\s+(LINE|SINE|DNA|LTR)')
    while True:
        l_now = f_rm.readline()
        if len(l_now) == 0:
            break
        
        m = re_rm_repeat.match(l_now)
        if m == None:
            continue
        f_out.write(l_now)

##---------------------------------------------------------------
## test
# if (len(sys.argv) < 2):
#     print "para error! need to use:\npython %s human19.rm\n" % os.path.split(sys.argv[0])[1]
#     sys.exit()

## rm2bed(sys.argv[1])
#get_te(sys.argv[1] + ".bed.sort")
