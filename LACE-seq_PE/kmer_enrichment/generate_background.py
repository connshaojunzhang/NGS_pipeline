import sys
import os
import random
import pandas as pd

iteration = 1000

stat = {}
for i in range(iteration):
    with open('temp_iter.bed', 'w') as out:
        for line in open(sys.argv[1], 'r'):
            s = line.strip().split('\t')
            for n in range(int(s[-1])):
                cnt = random.randint(int(s[1])+25, int(s[2])-25)
                out.writelines('\t'.join([s[0], str(cnt-25), str(cnt+25), "%s_%d"%(s[3], n), "0", s[5]]) + '\n')
    cmd = 'fastaFromBed -s -name -tab -fi /mnt/pub/work/duzc/p0.uCLIP-seq_srb_v2/1.Hela_PTB/0.ref/1.bowtie_index/mm9/mm9.fa -bed temp_iter.bed >temp_iter.fasta'
    os.system(cmd)
    stat[i] = {}
    for line in open('temp_iter.fasta', 'r'):
        seq = line.strip().split('\t')[-1].upper()
        for j in range(len(seq)-6):
            if seq[j:j+6].find('N') >= 0:
                continue
            if not seq[j:j+6] in stat[i]:
                stat[i][seq[j:j+6]] = 0
            stat[i][seq[j:j+6]] += 1

stat = pd.DataFrame(stat)
b = stat / stat.sum(axis=0)
b_mean = b.mean(axis=1)
b_std = b.std(axis=1, ddof=1)
for i in b_mean.index.tolist():
    print(i, b_mean[i], b_std[i], sep="\t")
                




