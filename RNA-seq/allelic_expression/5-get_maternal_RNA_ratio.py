# -*- coding: utf-8 -*-
"""
Created on Thu Jul 26 19:26:22 2018

@author: duzc
"""

import math

filter_chrom = ['chrX', 'chrY', 'chrM']

gene2type = {}
with open('summary', 'r') as infile:
    for line in infile:
        if line.startswith('type'):
            continue
        
        s = line.strip().split('\t')
        gene2type[s[2] +'|'+ s[0]] = s[3]

read_count = {} #[sample][gene]
with open('./sample_filter_gene_readCount.tsv', 'r') as infile:
    for line in infile:
        if line.startswith('Index'):
            title = line.strip().split('\t')
            for i in title:
                read_count[i] = {}
            continue
        s = line.strip().split('\t')
        gene = s[0]
        for sample, expr in zip(title, s[1:]):
            read_count[sample][gene] = int(expr)
        

           
stat = {} #stat[sample] = [dba, c57]
with open('gene_by_cells_allelic_reads.txt', 'r') as infile:
    for line in infile:
        if line.startswith('Index'):
            title = line.strip().split('\t')
            for i in title:
                stat[i] = [0, 0]
            continue
        s = line.strip().split('\t')
        gene = s[0]
        #only include atuo-chromosome !!!
        if gene2type[gene] in filter_chrom:
            continue
        for sample, reads in zip(title, s[1:]):
            count_key = sample
            if sum(map(int, reads.split('|') )) < 1:
                continue
            read1, read2 = map(int, reads.split('|'))
            #print(sample, count_key, gene)
            stat[sample][0] += math.ceil( read1 / (read1 + read2) * read_count[count_key][gene] )
            stat[sample][1] += math.ceil( read2 / (read1 + read2) * read_count[count_key][gene] )
            
            
            
with open('maternal_RNA_ratio.txt', 'w') as out:
    for sample in title:
        ratio = str( stat[sample][1] / sum(stat[sample]) )
        out.writelines(sample +'\t'+ '\t'.join(map(str, stat[sample])) +'\t'+ ratio +'\n')
        


        



