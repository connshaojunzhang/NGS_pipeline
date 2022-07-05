# -*- coding: utf-8 -*-
"""
Created on Fri Mar  9 14:44:46 2018

@author: pc
"""

import os

files = ['../1.data/'+i for i in os.listdir('../1.data/') if i.endswith('.bam')]
for file in files:
    prefix = file.split('/')[-1].split('.')[0]
    #print(prefix)
    cmd = 'samtools mpileup -O -l ../0.snp_ref/DBAsnps.txt %s >%s.mpileup'%(file, prefix)
    print(cmd)

