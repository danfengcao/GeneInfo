Gene Information
===========================
---
##Introduction

Code in this repository was used to generate GeneInfomation.txt which contain infomation as follows:

+ chrN 
+ start_codon 
+ end_codon 
+ symbol_of_chain: + or - 
+ transcript_number
+ gene_id gene_name gene_biotype
+ te_in_gene: gene_length overlapped_TE_length TE_fraction_in_this_gene
+ te_in_cds: cds_length_of_this_gene cds_length_overlapped_TE TE_fraction_in_cds
+ disease_gene: -(not in OMIM) year(added in OMIM in 1996)

Each line above stands for a column (seperated by '\t') in the output file, GeneInfomation.txt 

---
##Run program

To generate GeneInfo.txt, all you need to do is 3 simple steps.

1, clone GeneInfo project to your Linux environment.
>```
git clone https://github.com/danfengcao/GeneInfo.git
```

2, Download **Homo_sapiens.GRCh37.73.gtf.gz** from <ftp://ftp.ensembl.org/pub/release-73/gtf/homo_sapiens/Homo_sapiens.GRCh37.73.gtf.gz> and download **hg19.fa.out.gz.gz** from [RepeatMasker](http://www.repeatmasker.org/genomes/hg19/RepeatMasker-rm405-db20140131/hg19.fa.out.gz)
>```
cd GeneInfo/data
wget ftp://ftp.ensembl.org/pub/release-73/gtf/homo_sapiens/Homo_sapiens.GRCh37.73.gtf.gz
wget http://www.repeatmasker.org/genomes/hg19/RepeatMasker-rm405-db20140131/hg19.fa.out.gz
gunzip -c Homo_sapiens.GRCh37.73.gtf.gz > ensembl.gtf
gunzip -c hg19.fa.out.gz > human19.rm
```

3, Run the program and you will get the result in **GeneInfomation.txt**
>```
cd ..
python GeneInfo.py data/ensembl.gtf data/human19.rm data/newDiseaseGeneEachYear
```

---
Firstly written by gentle smart hansome dfcao ## 2014-12-20

If you have any question or suggestion, please send email to me(cdf4026176@aliyun.com).

如果您有任何疑问或建议，欢迎给发邮件给我（cdf4026176@aliyun.com）。