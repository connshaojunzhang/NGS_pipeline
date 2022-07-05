import sys

bg = { line.strip().split('\t')[0]:list(map(float, line.strip().split('\t')[1:])) for line in open(sys.argv[1], 'r')} #bg file

stat_peak = {}
kmer_num = 0
for line in open(sys.argv[2], 'r'): #fasta_tab file
    s = line.strip().split('\t')
    s[-1] = s[-1].upper()
    for j in range(len(s[-1])-6):
        if s[-1][j:j+6].find('N') >= 0:
            continue
        if not s[-1][j:j+6] in stat_peak:
            stat_peak[s[-1][j:j+6]] = 0
        stat_peak[s[-1][j:j+6]] += 1
        kmer_num += 1

for kmer in stat_peak:
    if bg[kmer][1] == 0:
        continue
    print(kmer, (stat_peak[kmer]/kmer_num - bg[kmer][0]) / bg[kmer][1], sep="\t")




