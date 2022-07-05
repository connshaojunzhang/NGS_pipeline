# -*- coding: utf-8 -*-
"""
Created on Fri Mar  9 17:27:58 2018

@author: pc
"""

import os

requiredQ = 30
index = {'A':0, 'C':1, 'G':2, 'T':3}

mpileups = ['../2.mpileups/'+i for i in os.listdir('../2.mpileups/') if i.endswith('.mpileup')]
for file in mpileups:
    prefix = file.split('/')[-1].split('.')[0]
    #if not prefix.find('WT-M2') > 0:
    #    continue

    with open(prefix+'.cellsum', 'w') as out:
        for line in open(file):
            ntCounts = [0] * 4
            chrom, pos, ref, nb, bases, quals, extra = line.strip().split('\t')
            nb = int(nb)
            for base, qual in zip(bases, quals):
                if ord(qual)-33 >= requiredQ:
                    if not base.upper() in index.keys():
                        #print(base)
                        continue
                    ntCounts[index[base.upper()]] += 1
            if sum(ntCounts) > 0:
                out.writelines('\t'.join([chrom, pos]) +'\t'+ '\t'.join(map(str, ntCounts)) +'\n')



