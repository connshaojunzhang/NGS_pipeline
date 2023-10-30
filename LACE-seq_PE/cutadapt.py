import sys
import os

path = sys.argv[1]
f1 = [ path+i for i in os.listdir(path) if i.endswith("_1.fq.gz") ]
f1.sort()
f2 = [ path+i for i in os.listdir(path) if i.endswith("_2.fq.gz") ]
f2.sort()

for i, j in zip(f1, f2):
    prefix = i.split("/")[-1].split("_")[0]
    cmd = f"""cutadapt -m 18 -j 8 --match-read-wildcards --max-n 4 --trim-n --times 2 -e 0.1 -O 3 -a NNNNAGATCGGAAGAGCAC -a NNNNAGATCGGAAGA -a GGAAGAGCACACGTC -a AGCACACGTCTGAAC -a ACGTCTGAACTCCAG -a TGAACTCCAGTCACC -a TCCAGTCACCATTGC -a TCACCATTGCTTATC -a ATTGCTTATCTCGTA -a TTATCTCGTATGCCG -a TCGTATGCCGTCTTC -a TGCCGTCTTCTGCTTG -a G{"{30}"} -a A{"{20}"} -a T{"{20}"} -G NNNNCAATCGNNNNNNNNTTCAGACGTGTGCTCTTCCGATCT -A NNNNAGATCGGAAGAGCGT -A NNNNAGATCGGAAGA -A GGAAGAGCGTCGTGT -A AGCGTCGTGTAGGGA -A CGTGTAGGGAAAGAG -A AGGGAAAGAGTGTAG -A AAGAGTGTAGATCTC -A TGTAGATCTCGGTGG -A ATCTCGGTGGTCGCC -A GGTGGTCGCCGTATCATT -A G{"{30}"} -A A{"{20}"} -A T{"{20}"} -o {prefix}_1.cutadapt.fq.gz -p {prefix}_2.cutadapt.fq.gz {i} {j} >{prefix}.cutadapt.log"""
    print(cmd)

    cmd=f"java -jar /home/liuzhe/Software/Trimmomatic-0.36/trimmomatic-0.36.jar PE -threads 8 -phred33 {prefix}_1.cutadapt.fq.gz {prefix}_2.cutadapt.fq.gz  {prefix}_1.paired.fq.gz {prefix}_1.unpaired.fq.gz {prefix}_2.paired.fq.gz {prefix}_2.unpaired.fq.gz LEADING:3 TRAILING:3 CROP:90 SLIDINGWINDOW:5:20 MINLEN:18"
    print(cmd)

    cmd = f"fastp -i {prefix}_1.paired.fq.gz -I {prefix}_2.paired.fq.gz -o {prefix}_1.trim.fq.gz -O {prefix}_2.trim.fq.gz --unpaired1 {prefix}_1.unpair.fq.gz --unpaired2 {prefix}_2.unpair.fq.gz -m --merged_out {prefix}.merge.fq.gz -l 18 -y -Y 30 -c --overlap_len_require 30 --overlap_diff_percent_limit 10 -U --umi_loc read1 --umi_len 4 -w 8 -h {prefix}.html -j {prefix}.json -x --poly_x_min_len 3"
    print(cmd)

    ## 2. rename
    cmd = f"python3 extract_umi.py {prefix}.merge.fq.gz {prefix}_2.trim.fq.gz {prefix}_2.unpair.fq.gz |gzip >{prefix}.merge_rename.fq.gz"
    print(cmd)
    cmd = f"bowtie2 -p 4 -x /media/ibm_disk/work/database/2.mouse/rRNA_reference/rRNA_reference.fa -U {prefix}.merge_rename.fq.gz --un-gz {prefix}.non_rRNA.fq.gz -S /dev/stdout 2>{prefix}.rRNA_log |samtools sort -@ 8 -o {prefix}.rRNA.sort.bam"
    print(cmd)







"""
path = "./1.trim_polyx/"
f1 = [ path+i for i in os.listdir(path) if i.endswith("_1.trim1.fq.gz") ]
f1.sort()
f2 = [ path+i for i in os.listdir(path) if i.endswith("_2.trim1.fq.gz") ]
f2.sort()

for i, j in zip(f1, f2):
    prefix = i.split("/")[-1].split("_")[0]
    # trim_adaptor
    if not os.path.exists("./2.trim_adaptor/"):
        os.mkdir("./2.trim_adaptor/")
    path_prefix = "./2.trim_adaptor/"+prefix

    cmd = f"cutadapt -m 18 -j 12 --times 3 -e 0.1 -O 6 -a NNNNAGATCGGAAGA -G NNNNTTCAGACGTGTGCTCTTCCGATCT -A NNNNAGATCGGAAGA -o {path_prefix}_1.trim2.fq.gz -p {path_prefix}_2.trim2.fq.gz {i} {j}>{path_prefix}.trim2.log"
    print(cmd)

    cmd = f"fastp -i {path_prefix}_1.trim2.fq.gz -I {path_prefix}_2.trim2.fq.gz -o {prefix}_1.trim.fq.gz -O {prefix}_2.trim.fq.gz --unpaired1 {prefix}_1.unpair.fq.gz --unpaired2 {prefix}_2.unpair.fq.gz --detect_adapter_for_pe --adapter_sequence AGATCGGAAGA --adapter_sequence_r2 AGATCGGAAGA  -m --merged_out {prefix}.merge.fq.gz -l 18 -y -Y 10 -c --overlap_len_require 30 --overlap_diff_percent_limit 10 -U --umi_loc per_read --umi_len 4 -w 8 -h {prefix}.html -j {prefix}.json"
    print(cmd)

    ## 2. rename
    cmd = f"python3 rename.py {prefix}.merge.fq.gz {prefix}_2.trim.fq.gz {prefix}_2.unpair.fq.gz |gzip >{prefix}.merge_rename.fq.gz"
    print(cmd)
    cmd = f"bowtie2 -p 12 --end-to-end -x /media/ibm_disk/work/database/2.mouse/rRNA_reference/rRNA_reference.fa -U {prefix}.merge_rename.fq.gz --un-gz {prefix}.non_rRNA.fq.gz -S /dev/stdout 2>{prefix}.rRNA_log |samtools sort -@ 8 -o {prefix}.rRNA.sort.bam"
    print(cmd)
"""
