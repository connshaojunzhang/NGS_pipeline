import sys
import os

path = sys.argv[1]
bams = [ path+i for i in os.listdir(path) if i.endswith(".sort.bam") ]
bams.sort()

for b in bams:
    prefix = b.split("/")[-1].split(".")[0]
    cmd = f"pureclip -i {b} -bai ../3.rmdup/merge/{prefix}.merge.sort.bam.bai -g /media/ibm_disk/work/database/2.mouse/NCBIM37.mm9_cleangeome_index/genome.NCBIM37.clean.fa -o {prefix}.cs.bed -or {prefix}.bd.bed -nt 16 -fis ./CL_motif/{prefix}.CL_motif.bed -nim 4"
    print(cmd)


