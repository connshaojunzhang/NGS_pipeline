import os
import sys
import gzip


path = sys.argv[1]
f1 = [ os.path.join(path, i) for i in os.listdir(path) if i.endswith("1.fastq.gz") or i.endswith("1.fq.gz") ]
f1.sort()
f2 = [ os.path.join(path, i) for i in os.listdir(path) if i.endswith("2.fastq.gz") or i.endswith("2.fq.gz") ]
f2.sort()

for i, j in zip(f1, f2):
    prefix1 = i.split('/')[-1].split('_')[0]
    prefix2 = j.split('/')[-1].split('_')[0]
    if prefix1[:-1] != prefix2[:-1]:
        print(i, j)
        exit()
    
    prefix = prefix1.rsplit("_", 1)[0]
    ## 1. mark UMI and trim adaptor 
    cmd = f"trim_galore --paired -j 7 --basename {prefix} {i} {j}"
    print(cmd)

    ## 2. rename
    #cmd = f"python3 rename.py {prefix}_2.trim.fq.gz {prefix}_2.unpair.fq.gz {prefix}.merge.fq.gz |gzip >{prefix}.merge_rename.fq.gz"
    #print(cmd)
    #cmd = f"bowtie2 -p 12 -x ./rRNA/rRNA_reference.fa -U {prefix}.merge_rename.fq.gz --un-gz {prefix}.non_rRNA.fq.gz 1> /dev/null 2> {prefix}.rRNA_log"
    #print(cmd)


