import os
import numpy as np

files = [ i for i in os.listdir() if i.endswith('.stat')]
for file in files:
    prefix = file.split('.')[0]
    m = []
    p = []
    for line in open(file):
        s = line.strip().split('\t')
        if int(s[6]) < 50:
            continue
        m.append(float(s[-2]))
        p.append(float(s[-1]))
    print(prefix, np.median(m), np.median(p), sep="\t" )




