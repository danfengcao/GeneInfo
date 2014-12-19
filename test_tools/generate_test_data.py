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
def generate_test_data(f_name, n):
    f_in = open(f_name)
    f_name_out = os.path.split(f_name)[1] + ".test"
    f_out = open(f_name_out, "w")
    
    chrs = []
    for i in range(1,23):
        chrs.append(str(i))
    chrs.append('X')
    chrs.append('Y')

    parts = ""
    for i in chrs:
        chrome = "chr" + i
        f_tmp_name = "file_" + str(chrome)
        grep = "grep -P '%s\\t' %s | head -n %s > %s" % (chrome, f_name, n, f_tmp_name)
        os.system(grep)
        parts += (f_tmp_name + " ")
        # f_tmp = open(f_tmp_name)
        # while True:
        #     l_now = f_tmp.readline()
        #     if len(l_now) == 0:
        #         break
        #     f_out.write(l_now)

    
    os.system("cat %s > %s" % (parts, f_name_out))
    os.system("rm %s" % parts)

#---------------------------------------------------------------
# test
if (len(sys.argv) < 3):
    print "para error! need to use:\npython %s human.19.sort.te n" % sys.argv[0]
    sys.exit()

generate_test_data(sys.argv[1], sys.argv[2])
