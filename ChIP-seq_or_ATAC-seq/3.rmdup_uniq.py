import os

files = [ '../2.mapping/'+i for i in os.listdir('../2.mapping/') if i.endswith('.sort.bam')]
files.sort()

for i in files:
    prefix = i.split('/')[-1].split('.')[0]
    cmd = 'java -jar ~/software/picard.jar MarkDuplicates I=%s O=%s.rmdup.sort.bam REMOVE_DUPLICATES=true M=%s.matrix'%(i, prefix, prefix)
    print(cmd)
    cmd = r'''samtools view -h -F 4 -F 256 -F 1024 -F 2048 -q 30 %s.rmdup.sort.bam |samtools sort -@ 8 -o %s.uniq.Mismatch3.rmdup.sort.bam '''%(prefix, prefix)
    print(cmd)
