# -*- coding: utf-8 -*-
"""
Created on Thu Mar  8 17:47:11 2018

@author: duzc
"""
#python3 1.STAR_PE_mapping.py $path_to_clean_data(no '/') $path_to_STAR_genome_index

import os 
import sys

path = sys.argv[1] #don't end with '/'
files = [path +'/'+ i for i in os.listdir(path) if i.endswith('.fq.gz')]
files.sort()

for i in range(0, len(files), 2):
    prefix1 = files[i].split('/')[-1].split('_')[0]
    prefix2 = files[i+1].split('/')[-1].split('_')[0]
    if prefix1 != prefix2:
        print("NOT PAIRED!!!", files[i], files[i+1], sep = "\t")
        exit()
    
    cmd = 'mkdir ./%s'%(prefix1)
    print(cmd)
    #os.system(cmd)
    cmd = 'STAR-2.6.1a --runThreadN 8 --genomeDir ./4.STAR_index/1.C57BL6J \
           --sjdbGTFfile gencode.vM1.annotation.gtf \
           --readFilesIn %s %s\
           --readFilesCommand zcat \
           --outFileNamePrefix ./%s/%s_ \
           --outSAMtype BAM Unsorted \
           --outSAMattributes All vG vA vW \
           --varVCFfile ./3.ASElux_snp/1.C57BL6J/snp.vcf \
           --waspOutputMode SAMtag --peOverlapNbasesMin 0 --peOverlapMMp 0.01'%(files[i], files[i+1], prefix1, prefix1)
    print(cmd)
    #os.system(cmd)   

    


