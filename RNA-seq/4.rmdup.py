import sys
import os

path = sys.argv[1]
files = [ path+i for i in os.listdir(path) if i.endswith('uniq.sort.bam')]
files.sort()

for i in files:
    prefix = i.split('/')[-1].split('.')[0]
    cmd = 'java -jar /media/ibm_disk/work/duzc/software/picard.jar MarkDuplicates I=%s O=%s.rmdup.uniq.sort.bam REMOVE_DUPLICATES=true M=%s.matrix'%(i, prefix, prefix)
    print(cmd)

