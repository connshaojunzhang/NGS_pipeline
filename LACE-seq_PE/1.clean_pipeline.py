import os
import sys
import gzip


path = sys.argv[1]
f1 = [ os.path.join(path, i) for i in os.listdir(path) if i.endswith("1.fastq.gz") or i.endswith("1.fq.gz") ]
f1.sort()
f2 = [ os.path.join(path, i) for i in os.listdir(path) if i.endswith("2.fastq.gz") or i.endswith("2.fq.gz") ]
f2.sort()

for i, j in zip(f1, f2):
    #prefix1 = i.split('/')[-1].rsplit('_', 1)[0]
    #prefix2 = j.split('/')[-1].rsplit('_', 1)[0]
    #if prefix1[:-1] != prefix2[:-1]:
    #    print(i, j)
    #    exit()
    
    prefix = i.split('/')[-1].rsplit("_", 1)[0]
    ## 1. mark UMI and trim adaptor 
    cmd = f"fastp -i {i} -I {j} -o {prefix}_1.trim.fq.gz -O {prefix}_2.trim.fq.gz --unpaired1 {prefix}_1.unpair.fq.gz --unpaired2 {prefix}_2.unpair.fq.gz --detect_adapter_for_pe -m --merged_out {prefix}.merge.fq.gz -e 20 -l 18 -y -Y 10 -c --overlap_len_require 10 --overlap_diff_percent_limit 10 -U --umi_loc per_read --umi_len 4 -w 8 -h {prefix}.html -j {prefix}.json -x --poly_x_min_len 5"
    print(cmd)

    ## 2. rename
    cmd = f"python3 rename.py {prefix}_2.trim.fq.gz {prefix}_2.unpair.fq.gz {prefix}.merge.fq.gz |gzip >{prefix}.merge_rename.fq.gz"
    print(cmd)
    cmd = f"bowtie2 -p 12 -x /media/ibm_disk/work/database/2.mouse/rRNA_reference/rRNA_reference.fa -U {prefix}.merge_rename.fq.gz --un-gz {prefix}.non_rRNA.fq.gz 1> /dev/null 2> {prefix}.rRNA_log"
    print(cmd)

