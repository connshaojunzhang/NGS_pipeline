import os

f1 = ['../1.cleandata/'+i for i in os.listdir('../1.cleandata/') if i.endswith('_val_1.fq.gz')]
f2 = ['../1.cleandata/'+i for i in os.listdir('../1.cleandata/') if i.endswith('_val_2.fq.gz')]
f1.sort()
f2.sort()

for i, j in zip(f1, f2):
    prefix1 = i.split('/')[-1].split('_')[0]
    prefix2 = j.split('/')[-1].split('_')[0]
    if prefix1 != prefix2:
        print('NOT PAIRED!!!')
        continue
    #print(prefix1, prefix2)
    cmd = f"hisat2 -x /media/ibm_disk/work/database/2.mouse/NCBIM37.mm9_cleangeome_index/genome.NCBIM37.clean.fa --dta-cufflinks --no-mixed --no-discordant -p 8 -1 {i} -2 {j} -S /dev/stdout 2>{prefix1}.log |samtools sort -@ 8 -o {prefix1}.sort.bam"
    print(cmd)

