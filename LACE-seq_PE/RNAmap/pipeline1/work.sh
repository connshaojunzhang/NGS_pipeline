python3 1.generate_bins.py ../7.AS/Srsf1_AS/SE.MATS.JC.txt |sortBed >se_bins.bed
bedtools coverage -a ./se_bins.bed -b ../../LACE-seq_mouse_SRSF1_SRSF10/3.rmdup/merge/Srsf1_merge.rmdup.sort.bam -s -f 0.5 -split -c>se_bins.cov


