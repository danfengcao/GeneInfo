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

def te_percentage(f_name_gene, f_name_rm):
    print "calculate te percentage of te in each gene..."
    f_out_name = os.path.split(f_name_gene)[1] + ".fraction"
    f_out = open(f_out_name, 'w')
    f_tmp_name = "file" + str(hash(f_name_gene))
    
    print "use bedtools to get intersect region..."
    os.system("bedtools intersect -a " + f_name_gene + " -b " + f_name_rm + " > " + f_tmp_name)
    
    f_gene = open(f_name_gene)
    f_tmp = open(f_tmp_name)
    re_bed = re.compile('^chr(?P<chr>[\dxXyY]{1,2})\s+(?P<start>\d+)\s+(?P<end>\d+)\s+(?P<suffix>.*)')
    line1 = f_gene.readline()
    line2 = f_tmp.readline()
    m1 = re_bed.match(line1)
    m2 = re_bed.match(line2)

    while True:
        if len(line1) == 0 or len(line2) == 0:
            break

        m1 = re_bed.match(line1)
        m2 = re_bed.match(line2)

        #print cmp(m1.group("chr"), m2.group("chr"))
        while len(line1) != 0 and len(line2) != 0 and cmp(m1.group("chr"), m2.group("chr")) != 0:
            chr1 = chrom2num(m1.group("chr"))
            chr2 = chrom2num(m2.group("chr"))
            #print chr1, "" , chr2
            if chr1 < chr2:
                te_fraction = 0
                l_out = "chr%s\t%s\t%s\t%s\tte_per_gene %.4f\n" % (m1.group("chr"), m1.group("start"), m1.group("end"), m1.group("suffix"), te_fraction)
                f_out.write(l_out)

                line1 = f_gene.readline()
                m1 = re_bed.match(line1)
            elif chr1 > chr2:
                line2 = f_tmp.readline()
                m2 = re_bed.match(line2)

        while len(line1) != 0 and len(line2) != 0 and string.atoi(m1.group("end")) < string.atoi(m2.group("start")):
            te_fraction = 0
            l_out = "chr%s\t%s\t%s\t%s\tte_per_gene %.4f\n" % (m1.group("chr"), m1.group("start"), m1.group("end"), m1.group("suffix"), te_fraction)
            f_out.write(l_out)

            line1 = f_gene.readline()
            m1 = re_bed.match(line1)
        
        if len(line1) != 0 and len(line2) != 0:
            gene_len = string.atoi(m1.group("end")) - string.atoi(m1.group("start")) + 1
            overlap_len = 0
            while len(line1) != 0 and len(line2) != 0 and string.atoi(m1.group("end")) >= string.atoi(m2.group("start")):
                if cmp(m1.group("chr"), m2.group("chr")) != 0:
                    break
                elif string.atoi(m1.group("start")) > string.atoi(m2.group("end")):
                    line2 = f_tmp.readline()
                    m2 = re_bed.match(line2)
                elif string.atoi(m1.group("start")) >= string.atoi(m2.group("start")):
                    overlap_len += (string.atoi(m2.group("end")) - string.atoi(m1.group("start")) + 1)
                    line2 = f_tmp.readline()
                    m2 = re_bed.match(line2)
                elif string.atoi(m1.group("end")) >= string.atoi(m2.group("end")):
                    overlap_len += (string.atoi(m2.group("end")) - string.atoi(m2.group("start")) + 1)
                    line2 = f_tmp.readline()
                    m2 = re_bed.match(line2)
                elif string.atoi(m1.group("end")) < string.atoi(m2.group("end")) and string.atoi(m1.group("end")) >= string.atoi(m2.group("start")):
                    overlap_len += (string.atoi(m1.group("end")) - string.atoi(m2.group("start")) + 1)
                    line2 = f_tmp.readline()
                    m2 = re_bed.match(line2)
                    
            te_fraction = float(overlap_len) / gene_len
            l_out = "chr%s\t%s\t%s\t%s\tte_per_gene %.4f\n" % (m1.group("chr"), m1.group("start"), m1.group("end"), m1.group("suffix"), te_fraction)
            f_out.write(l_out)
            line1 = f_gene.readline()
            m1 = re_bed.match(line1)

            if len(line1) != 0 and len(line2) != 0:
                while chrom2num(m1.group("chr")) < chrom2num(m2.group("chr")):
                    m1 = re_bed.match(line1)
                    te_fraction = 0
                    l_out = "chr%s\t%s\t%s\t%s\tte_per_gene %.4f\n" % (m1.group("chr"), m1.group("start"), m1.group("end"), m1.group("suffix"), te_fraction)
                    f_out.write(l_out)
                    line1 = f_gene.readline()

        

    while len(line1) != 0:
        m1 = re_bed.match(line1)
        te_fraction = 0
        l_out = "chr%s\t%s\t%s\t%s\tte_per_gene %.4f\n" % (m1.group("chr"), m1.group("start"), m1.group("end"), m1.group("suffix"), te_fraction)
        f_out.write(l_out)
        line1 = f_gene.readline()
    
    f_out.close
    f_gene.close
    f_tmp.close
    

#---------------------------------------------------------------
# test
# if (len(sys.argv) < 3):
#     print "para error! need to use:\npython %s ensembl.gtf.tranNum.sort human19.rm.bed.sort.te\n" % os.path.split(sys.argv[0])[1]
#     sys.exit()

# te_percentage(sys.argv[1], sys.argv[2])
