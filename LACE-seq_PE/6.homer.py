import sys
import os

path = sys.argv[1]
cs_bed = [ path+i for i in os.listdir(path) if i.endswith(".cs.bed") ]
cs_bed.sort()

extend = 50

for bed in cs_bed:
    prefix = bed.split("/")[-1].split(".")[0]
    cmd = r"""awk 'BEGIN{OFS="\t"}{print $1, $2-50, $3+50, "cs_"NR, 0, $6}' %s |bedtools intersect -s -u -a - -b exon_region.bed > %s.exon_cs.bed"""%(bed, prefix)
    #print(cmd)
    cmd = f"bedtools shuffle -i {prefix}.exon_cs.bed -g /media/ibm_disk/work/database/2.mouse/NCBIM37.mm9_cleangeome_index/chrNameLength.txt -incl exon_region.bed >{prefix}.bg.bed"
    #print(cmd)
    cmd = f"findMotifsGenome.pl {prefix}.exon_cs.bed  mm9 motif_{prefix} -rna -len 6 -bg {prefix}.bg.bed -S 10 -size 15"
    print(cmd)
    #print()

