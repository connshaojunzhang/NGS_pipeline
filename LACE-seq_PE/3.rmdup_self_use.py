import sys
import os

import pysam

path = sys.argv[1]
bams = [ path+i for i in os.listdir(path) if i.endswith(".sort.uniq.bam") ]
bams.sort()

for b in bams:
    prefix = b.split("/")[-1].split(".")[0]
    out_name = f"{prefix}.rmdup.uniq.sort.bam"
    with pysam.AlignmentFile(b, "r") as infile, pysam.AlignmentFile(out_name, "wb", template=infile) as outfile:
        stat = {}
        for read in infile:
            key1 = "|".join([read.reference_name, str(read.reference_start), str(read.reference_end)])
            key2 = read.qname.split("_")[-1]
            if not key1 in stat:
                stat[key1] = set()

            if not key2 in stat[key1]:
                stat[key1].add(key2)
                outfile.write(read)

    cmd = f"samtools index {out_name}"
    os.system(cmd)
    #break
