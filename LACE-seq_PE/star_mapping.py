import sys
import os

path = sys.argv[1]
f1 = [ path+i for i in os.listdir(path) if i.endswith("non_rRNA.fq.gz") ]
f1.sort()
#f2 = [ path+i for i in os.listdir(path) if i.endswith("2.fq.gz") ]
#f2.sort()

for i  in f1:
    prefix = i.split("/")[-1].split(".")[0]
    if not os.path.exists(prefix):
        os.mkdir(prefix)

    cmd = f"""STAR --runThreadN 20 --runMode alignReads --readFilesCommand zcat --outSAMtype BAM SortedByCoordinate --outBAMsortingThreadN 12 --genomeDir /media/ibm_disk/work/database/2.mouse/NCBIM37.mm9_cleangeome_index/ --sjdbGTFfile /media/ibm_disk/work/database/2.mouse/Gencode.vM1/gencode.vM1.annotation.gtf --outReadsUnmapped Fastx --outSJfilterReads Unique --alignEndsType Extend5pOfRead1 --outFilterMismatchNoverLmax 0.04 --outFilterMismatchNmax 999 --outFilterMultimapNmax 1  --readFilesIn {i} --outFileNamePrefix ./{prefix}/{prefix}. --outSAMattributes All """
    print(cmd)
    cmd = rf"""ln -s ./{prefix}/{prefix}.Aligned.sortedByCoord.out.bam ./{prefix}.sort.uniq.bam"""
    print(cmd)

    cmd = f"samtools index {prefix}.sort.uniq.bam"
    print(cmd)

