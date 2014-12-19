#!/usr/bin/python
##-------------------------------------------------------------------------
## Description: reserve one piece of overlapped region.
## firstly written by dfcao ## 2014/12/18 ##
##--------------------------------------------------------------------------

import re
import sys
import os
import string

def filt_duplicate(f_name):
    print "\nfilt duplicate region, reserve one piece...\n"

    f_in = open(f_name)
    f_out_name = os.path.split(f_name)[1] + ".uniq"
    f_out = open(f_out_name, 'w')

    chr_last = "0"
    st_last = 0
    en_last = 0

    re_bed = re.compile('^chr(?P<chr>[\dxXyY]{1,2})\s+(?P<start>\d+)\s+(?P<end>\d+)\s+')
    while True:
        l_now = f_in.readline()
        if len(l_now) == 0:
            break
        m = re_bed.match(l_now)
        if m == None:
            continue
	chr_now = m.group("chr")
	st_now = string.atoi(m.group("start"))
        en_now = string.atoi(m.group("end"))

	if cmp(chr_now, chr_last) != 0:
            f_out.write("chr%s\t%s\t%s\tTE\n" % (chr_now, st_now, en_now))
	    chr_last = chr_now
	    st_last = st_now
            en_last = en_now
	else:
	    if en_now <= en_last:
                continue
	    elif en_now > en_last:
		if st_now <= en_last:
		    st_now = en_last +1
		    f_out.write("chr%s\t%s\t%s\tTE\n" % (chr_now, st_now, en_now))
		else:
		    f_out.write("chr%s\t%s\t%s\tTE\n" % (chr_now, st_now, en_now))
		chr_last = chr_now
                st_last = st_now
                en_last = en_now

##-----------------------------------------
## test
# if (len(sys.argv) < 2):
#     print "para error! need to use:\npython %s human19.rm.sort.te" % sys.argv[0]
#     sys.exit()

# filt_duplicate(sys.argv[1])
