# -*- coding: utf-8 -*-
"""
Created on Wed Feb 28 15:47:20 2018

@author: pc
"""
import sys

gene2snps = {}
with open(sys.argv[1], 'r') as infile:
    for line in infile:
        s = line.strip().split('\t')
        if s[-1] == ".":
            continue
        #if s[8] in ('gene', 'transcript'):
        #    continue
        gene_id = s[-1].split('"')[1]
        gene_name = s[-1].split('"')[9]
        label = gene_name +'|'+ gene_id
        if label not in gene2snps:
            gene2snps[label] = set([])
        gene2snps[label].add((s[0], s[2]))

#out = open('validated_mm9_refseq_snp2genes.txt', 'w')
for gene in sorted(gene2snps):
    print(gene + '\t' + str(len(gene2snps[gene])) +'\t'+ \
                   ";".join([":".join(map(str, [c,p])) for c,p in gene2snps[gene]]))
#out.close()

