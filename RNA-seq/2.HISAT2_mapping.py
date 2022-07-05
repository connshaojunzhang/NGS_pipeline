import sys
import os

path = sys.argv[1]
read1 = [ path+i for i in os.listdir(path) if i.endswith('rmrRNA.fq.1.gz') ]
read1.sort()
read2 = [ path+i for i in os.listdir(path) if i.endswith('rmrRNA.fq.2.gz') ]
read2.sort()

#print(len(read1), len(read2))
for i, j in zip(read1, read2):
    prefix1 = i.split('/')[-1].split('_')[0]
    prefix2 = j.split('/')[-1].split('_')[0]
    if prefix1 != prefix2:
        print(prefix1, prefix2)
    cmd = f"hisat2 --dta -p 8 -x ../../../p1.early-embryo_srb/0.ref/7.HISAT2_index/1.C57BL6J/NCBIM37.mm9 -1 {i} -2 {j} --known-splicesite-infile ../../../p1.early-embryo_srb/0.ref/3.Genome_annotation/splice.txt -S /dev/stdout 2>{prefix1}.log |samtools sort -@ 8 -o {prefix1}.sort.bam"
    print(cmd)
