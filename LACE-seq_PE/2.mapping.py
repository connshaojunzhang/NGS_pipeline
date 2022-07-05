import os
import sys

path = sys.argv[1]
f1 = [ path+i for i in os.listdir(path) if i.endswith('.non_rRNA.fq.gz')]
#f2 = ['../1.cleandata/'+i for i in os.listdir('../1.cleandata/') if i.endswith('_val_2.fq.gz')]
f1.sort()
#f2.sort()

for f in f1:
    prefix1 = f.split('/')[-1].rsplit('.', 3)[0]
    cmd = f"hisat2 -x /media/ibm_disk/work/database/2.mouse/NCBIM37.mm9_cleangeome_index/genome.NCBIM37.clean.fa --no-softclip -p 8 --known-splicesite-infile ./mouse_ss.txt -U {f} -S /dev/stdout 2>{prefix1}.log |samtools sort -@ 8 -o {prefix1}.sort.bam"
    print(cmd)
    cmd = f"samtools index {prefix1}.sort.bam"
    print(cmd)

