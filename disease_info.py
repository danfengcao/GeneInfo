#!/usr/bin/python 
##-------------------------------------------------------------------------
## Description:add info of disease.
## firstly written by dfcao ## 2014/12/17 ##
##--------------------------------------------------------------------------

import os
import sys
import re

def disease_info(f_name_tran_num, disease_gene_year):
    print "add infomation of disease..."

    f_out = open(os.path.split(f_name_tran_num)[1] + ".disease", "w")
    f_disease = open(disease_gene_year)
    years = range(1996, 2014)
    disease = {}
    for i in years:
        while True:
            l_now = f_disease.readline()
            l_now = l_now.strip()
            if len(l_now) == 0:
                break
            if cmp(l_now, str(i+1)) == 0:
                break
            disease[l_now] = i

    print "%d disease related genes" % len(disease)

    f_tran_num = open(f_name_tran_num)
    i = 0
    re_disease = re.compile('^[\w\.\-]+\s+.*gene_name "(?P<gene_name>[\w\-\.\:]+)";\s+')
    while True:
        l_now = f_tran_num.readline()
        if len(l_now) == 0:
            break

        m = re_disease.match(l_now)
        if m == None:
            print "ensembl format error.."
            
        l_out = ""
        #print m.group("gene_name")
        try:
            if m.group("gene_name") in disease:
                l_out = l_now.strip() + "\t" + str(disease[m.group("gene_name")]) + "\n"
                i += 1
            else:
                l_out = l_now.strip() + "\t-\n"
        except AttributeError:
            print l_out
        f_out.write(l_out)
           
    f_out.close
    print i

##---------------------------------------------------------------
## test
# if (len(sys.argv) < 3):
#     print "para error! need to use:\npython %s ensembl.gtf.tranNum.sort.fraction newDiseaseGeneYear\n" % sys.argv[0]
#     sys.exit()

# disease_info(sys.argv[1], sys.argv[2])
