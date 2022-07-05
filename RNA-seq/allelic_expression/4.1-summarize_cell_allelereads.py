# -*- coding: utf-8 -*-
"""
Created on Fri Mar  2 10:30:21 2018

@author: pc
"""

import os

snp_to_gene_file = 'validated_mm9_GENCODE_snp2genes.txt'
validated_snp_file = 'validated_dba_c57_snps.txt'

snp2gene = {}
genes=[]
for line in open(snp_to_gene_file):
    parts = line.strip().split("\t")
    gene, count, snps = parts
    genes.append(gene)
    for snp in snps.split(";"):
        chrom, pos = snp.split(":")
        if not chrom in snp2gene:
            snp2gene[chrom]={}
        if not pos in snp2gene[chrom]:
            snp2gene[chrom][pos] = []
        snp2gene[chrom][pos].append(gene)
genes.sort()

snp2allele = {}
removed=0
nts = {'A':2, 'C':3, 'G':4, 'T':5, 'N':8 }
for line in open(validated_snp_file):
    parts = line.strip().split("\t")
    chrom, pos, c57, cast = parts[:4]
    if cast.count(",") > 0: 
        removed+=1
        continue
    if not chrom in snp2allele:
        snp2allele[chrom]={}
    snp2allele[chrom][pos] = (nts[c57], nts[cast])
print ('%i snps removed' % removed)

def classify_gene(castreads, c57reads):# needs to be renamed to cast and c57 reads, since we have reciprical crosses
    tot = float(castreads+c57reads)
    if castreads >= 2 and c57reads >= 2 and min([castreads/tot, c57reads/tot]) > 0.02:
        return (0, 'biallelic')
    elif castreads >=2 and castreads/tot > 0.98:
        return (1, 'dba_monoallelic')
    elif c57reads >=2 and c57reads/tot > 0.98:
        return (2, 'c57_monoallelic')
    else:
        return (3, 'no_call')

for file in os.listdir('0.cellsums'):
    gene_counts = {} #gene: cast, c57
    for line in open('0.cellsums/' + file):
        s = line.strip().split("\t")
        chrom, pos, a, c, g, t = s
        
        if chrom in snp2gene and pos in snp2gene[chrom]:
            for gene in snp2gene[chrom][pos]:
                if not gene in gene_counts:
                    gene_counts[gene] = [0, 0]
                
                if pos in snp2allele[chrom]:
                    c57, cast = snp2allele[chrom][pos]
                    gene_counts[gene][0] += int(s[cast])
                    gene_counts[gene][1] += int(s[c57])
                else:
                    pass
    out = open('./1.genesums/' + file.split('.')[0] +'.genesums', 'w')
    for gene in genes:
        if gene in gene_counts:
            acall = classify_gene(gene_counts[gene][0], gene_counts[gene][1])
            out.writelines('\t'.join([gene, '\t'.join(map(str,gene_counts[gene])), acall[1]]) +'\n')
    out.close()

                
            



