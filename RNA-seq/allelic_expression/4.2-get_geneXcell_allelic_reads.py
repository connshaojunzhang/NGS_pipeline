# -*- coding: utf-8 -*-
"""

Created on Thur July  2 15:11:16 2018

@author: duzc
"""

import os


samples = [i for i in os.listdir('./1.genesums/') if i.endswith('.genesums')]
samples.sort()
samples = samples[41:] + samples[:29] + samples[35:41] + samples[29:35]
print(samples)

files = [ './1.genesums/'+i for i in os.listdir('./1.genesums/') if i.endswith('.genesums') ]
data = {} #data[gene]
for file in files:
    for line in open(file):
        #print(file)
        gene, dba, c57, acall = line.strip().split('\t')
        if not gene in data:
            data[gene] = {}
        data[gene][ file.split('/')[-1] ] = (dba, c57)

out = open("gene_by_cells_allelic_reads.txt", 'w')
temp = [ '.'.join(i.split('.')[0].split('-')) for i in samples]
out.write('\t'.join(temp) + '\n')
for gene in sorted(data):
    out.writelines(gene +"\t"+ "\t".join(["%s|%s"%data[gene].get(sample, (0,0)) for sample in samples]) +'\n')
out.close()






