# -*- coding: utf-8 -*-
"""
Created on Sat Mar 24 13:38:32 2018

@author: pc
"""

import sys

cutoff = {'exon':1, 'fpkm':0.3, 'length':200}

#file = '../0.data/1.P0_T1.allInfor'
file = sys.argv[1]
out = open(file.split('.allInfor')[0]+'.firstFilter', 'w')
for line in open(file):
    s = line.split('\t')
    fpkm = map(float, s[9:])
    location = s[7].split(':')
    exon_num = location[-2]
    length = location[-1]
    if max(fpkm) > 0.3 and int(exon_num) > 1 and int(length) > 200:
        print(location[0], '\t'.join(location[2].split('-')), s[3]+":"+s[7], '.', location[1], sep="\t")
out.close()

