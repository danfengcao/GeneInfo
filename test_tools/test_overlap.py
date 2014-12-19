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
# test overlap
def test_overlap(f_name):
    f_in = open(f_name)
    re_bed = re.compile('^chr(?P<chr>\w+)\s+(?P<start>\d+)\s+(?P<end>\d+)\s+')
    last_end = 1000000000000
    last_line = ""
    while True: 
        l_now = f_in.readline()
        if len(l_now) == 0:
            break
        m = re_bed.match(l_now)
        if string.atoi(m.group("start")) <= last_end:
            print last_line
            print l_now
            print "#-------------------#"

        last_end = string.atoi(m.group("end"))
        last_line = l_now

#---------------------------------------------------------------
# test
if (len(sys.argv) < 2):
    print "para error! need to use:\npython %s human.19.sort.te" % sys.argv[0]
    sys.exit()

test_overlap(sys.argv[1])
