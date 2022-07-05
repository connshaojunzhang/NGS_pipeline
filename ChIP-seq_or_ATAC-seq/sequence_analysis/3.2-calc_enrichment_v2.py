import sys

bg = { line.strip().split('\t')[0]:list(map(float, line.strip().split('\t')[1:])) for line in open(sys.argv[1]) }
peak = { line.strip().split('\t')[0]:float(line.strip().split('\t')[1]) for line in open(sys.argv[2]) }

for kmer in peak:
    print(kmer, (peak[kmer]-bg[kmer][0])/bg[kmer][1], sep="\t")




