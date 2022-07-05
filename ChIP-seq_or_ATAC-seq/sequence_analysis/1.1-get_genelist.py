import sys
import os

cmd = "bedtools intersect -s -a %s -b ./peaks.uaRNA.bed -u"%(sys.argv[2])
genelist = { line.strip().split('\t')[3]:1 for line in os.popen(cmd).read().strip().split('\n') }

for line in open(sys.argv[1]):
    s = line.strip().split('\t')
    if genelist.get(s[3], 0):
        print(line.strip())



