import os

f1 = ['../1.cleandata/'+i for i in os.listdir('../1.cleandata/') if i.endswith('1.paired.fq.gz')]
f2 = ['../1.cleandata/'+i for i in os.listdir('../1.cleandata/') if i.endswith('2.paired.fq.gz')]
f1.sort()
f2.sort()

for i, j in zip(f1, f2):
    prefix1 = i.split('/')[-1].split('.')[0][:-1]
    prefix2 = j.split('/')[-1].split('.')[0][:-1]
    if prefix1 != prefix2:
        print('NOT PAIRED!!!')
        continue
    #print(prefix1, prefix2)
    cmd = 'bwa mem -t 4 /media/ibm_disk/work/database/GRCh37.p13/GRCh37.p13.genome.fa %s %s |samtools sort -@ 8 -o %s.sort.bam '%(i, j, prefix1[:-1])
    print(cmd)

