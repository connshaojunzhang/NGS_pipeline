# -*- coding: utf-8 -*-
"""
Created on Sat Mar 10 09:55:59 2018

@author: pc
"""

import os, sys

folders = [i for i in os.listdir() if os.path.isdir(i)]
snpstats = {}  #genotype:chrom:pos
chrompos = set([])
for folder in folders:
    genotype = folder.split('.')[-1]
    snpstats[genotype] = {}
    for file in os.listdir(folder):
        if not file.endswith('.cellsum'):
            continue
        print(os.path.join(folder, file))
        for line in open(os.path.join(folder, file)):
            chrom, pos, a, c, g, t = line.strip().split('\t')
            chrompos.add(':'.join([chrom, pos]))
            if not chrom in snpstats[genotype]:
                snpstats[genotype][chrom] = {}
            if not pos in snpstats[genotype][chrom]:
                snpstats[genotype][chrom][pos] = [0]*8
            for idx, val in enumerate(map(int, [a, c, g, t])):
                snpstats[genotype][chrom][pos][idx] += val
                if val > 0:
                    snpstats[genotype][chrom][pos][idx+4] += 1

alleles = {}
for line in open(sys.argv[1]):
    if line[0] == "#":
        continue
    s = line.strip().split('\t')
    if not 'chr'+':'.join(s[:2]) in chrompos:
        continue
    if not 'chr'+s[0] in alleles:
        alleles['chr'+s[0]] = {}
    alleles['chr'+s[0]][s[1]] = (s[3], s[4])

for folder in folders:
    genotype = folder.split('.')[-1]
    with open('snpstat_'+genotype+'.txt', 'w') as out:
        for cp in sorted(chrompos):
            chrom, pos = cp.split(':')
            c57allele, dballele = alleles[chrom][pos]
            out.write('\t'.join([chrom, pos, c57allele, dballele]) + '\t')
            out.write('\t'.join(map(str, snpstats[genotype][chrom].get(pos, [0]*8))) +'\n')  











