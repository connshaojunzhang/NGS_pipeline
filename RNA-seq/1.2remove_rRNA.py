import sys
import os

path = sys.argv[1]
f1 = [ path+i for i in os.listdir(path) if i.endswith("1.clean.fq.gz") ]
f1.sort()
f2 = [ path+i for i in os.listdir(path) if i.endswith("2.clean.fq.gz") ]
f2.sort()

for i, j in zip(f1, f2):
    prefix = i.split('/')[-1].split('_')[0]
    cmd = f"bowtie2 -x /media/ibm_disk/work/database/2.mouse/rRNA_reference/rRNA_reference.fa -1 {i} -2 {j} --very-sensitive-local -I 1 -X 1000 -p 8 --un-conc-gz {prefix}_rmrRNA.fq.gz -S /dev/null 2>{prefix}.log"
    print(cmd)


