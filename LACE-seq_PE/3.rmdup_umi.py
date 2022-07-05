import sys
import os

path = sys.argv[1]
bam = [ path+i for i in os.listdir(path) if i.endswith('.sort.bam') ]
bam.sort()

for b in bam:
    prefix = b.split('/')[-1].split('.')[0]
    cmd = f"umi_tools dedup -I {b} --output-stats={prefix}.dedup -S {prefix}.rmdup.sort.bam --method unique"
    print(cmd)
    #cmd = f"bamToBed -i {prefix}.rmdup.sort.bam >{prefix}.rmdup.sort.bed"
    #print(cmd)

