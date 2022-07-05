import os
import sys

files = [i for i in os.listdir() if i.endswith('.enrichment') ]
files.sort()

top_n = int(sys.argv[1])
stat = {}
for i in files:
    n = 0
    for line in open(i):
        s = line.strip().split('\t')
        if not s[0] in stat:
            stat[s[0]] = []
        n += 1
        if n >= top_n:
            break

for i in files:
    for line in open(i):
        s = line.strip().split('\t')
        if s[0] in stat:
            stat[s[0]].append(s[-1])

for key in stat:
    print(key, '\t'.join(stat[key]), sep="\t")
        
    



