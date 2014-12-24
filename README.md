Gene Information
===========================
---
##Introduction

Code in this repository was used to generate GeneInfo.txt which contain infomation as follows:

+ chrN 
+ start_codon 
+ end_codon 
+ symbol_of_chain: + or - 
+ transcript_number
+ gene_id gene_name gene_biotype
+ te_in_gene: gene_length overlapped_TE_length TE_fraction_in_this_gene
+ te_in_cds: cds_length_of_this_gene cds_length_overlapped_TE TE_fraction_in_cds
+ disease_gene: -(not in OMIM) year(added in OMIM in 1996)

Each line above stands for a column (seperated by '\t') in the output file, GeneInfo.txt 

---
##Run program

To generate GeneInfo.txt, all you need to do is 3 simple steps.

1. Download **Homo_sapiens.GRCh37.73.gtf.gz** from <ftp://ftp.ensembl.org/pub/release-73/gtf/homo_sapiens/Homo_sapiens.GRCh37.73.gtf.gz>

2. Download **hg19.fa.out.gz.gz** from [RepeatMasker](http://www.repeatmasker.org/genomes/hg19/RepeatMasker-rm405-db20140131/hg19.fa.out.gz)

3. Input command

>```
gunzip -c Homo_sapiens.GRCh37.73.gtf.gz > ensembl.gtf
gunzip -c hg19.fa.out.gz.gz > human19.rm
python GeneInfo.py ensembl.gtf human19.rm newDiseaseGeneEachYear
```


---
Firstly written by gentle smart hansome dfcao ## 2014-12-20