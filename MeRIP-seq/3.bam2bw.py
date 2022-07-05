import os
import sys

path = sys.argv[1]
files = [ os.path.join(path, i) for i in os.listdir(path) if i.endswith('.bam') ]
files.sort()

for i in files:
    prefix = i.split('/')[-1].split('.')[0]
    cmd = 'samtools index %s'%(i)
    print(cmd)
    #if prefix.find('hPTB') >= 0:
    #    cmd = 'bamCoverage -p 20 --binSize 5 --normalizeUsing RPKM -b %s -o %s.bw'%(i, prefix)
    #--normalizeUsing
    #else:
    cmd = 'bamCoverage -p 20 --binSize 1 --normalizeUsing CPM -b %s -o %s.bw'%(i, prefix)
    print(cmd)

