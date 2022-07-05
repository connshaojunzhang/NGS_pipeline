import sys
import os

path, genome_size = sys.argv[1:]

rmdup_bam = [ path+i for i in os.listdir(path) if i.endswith(".sort.bam") ]

for b in rmdup_bam:
    prefix = b.split('/')[-1].split('.')[0]
    cmd = f"bedtools genomecov -scale 1 -bg -split -ibam {b} -g {genome_size} >{prefix}.bdg"
    print(cmd)
    cmd = f"LC_COLLATE=C sort -k1,1 -k2,2n {prefix}.bdg >{prefix}.sort.bdg"
    print(cmd)
    cmd = f"bedGraphToBigWig {prefix}.sort.bdg {genome_size} {prefix}.rmdup.bw"
    print(cmd)


