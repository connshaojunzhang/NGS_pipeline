import sys

reads = {}
for line in open(sys.argv[1]):
    s = line.strip().split('\t')
    for i in s[-5].split(','):
        reads[i] = s[8]

out1 = open('HeLa_merge.select_RI.plus.bed', 'w')
out2 = open('HeLa_merge.select_RI.minus.bed', 'w')
out1.write('track graphType=arc\n')
out2.write('track graphType=arc\n')
infile = open(sys.argv[2])
for line in infile:
    if line.startswith('track'):
        #print(line.strip())
        continue
    s = line.strip().split('\t')
    s2 = infile.readline().strip().split('\t')
    if reads.get(s[3], 0) == '+':
        print(s[0], s[1], s2[2], s[3], 0, "+", sep="\t", file=out1)
    elif reads.get(s[3], 0) == '-':
        print(line.strip(), sep="\t", file=out2)
infile.close()
out1.close()
out2.close()


