import sys
import os
#Piranha_1_EXON::chr1:11882-11932(+)	AGCCTTTTCTTTGACCTCTTCTTTCTGTTCATGTGTATTTGCTGTCTCTT

cmd = 'fastaFromBed -s -tab -name -bed %s -fi ../../p5.ssDNA-seq_mouse_yxh/0.ref/4.bowtie_index/GRCh37.p13.chrom.fa'%(sys.argv[1])

stat = {}
k = 6
for line in os.popen(cmd).read().strip().split('\n'):
    s = line.strip().split('\t')
    region = s[0].split('::')[0].split('_')[-1]
    if not region in stat:
        stat[region] = {}
    for j in range(len(s[1])-6):
        kmer = s[1][j:j+k]
        if kmer.find('N') >= 0:
            continue
        if not kmer in stat[region]:
            stat[region][kmer] = 0
        stat[region][kmer] += 1

for region in stat:
    out = open(region+'.txt', 'w')
    for kmer in stat[region]:
        outline = kmer +'\t'+ str(stat[region][kmer]/sum(stat[region].values()))
        out.write(outline + '\n')
    out.close()


