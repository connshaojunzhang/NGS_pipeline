rmats2sashimiplot --l1 cKO --l2 WT -o ./Srsf2_AS_uniq/ -t SE -e ./select_se_events.txt --b2 ../4.rmdup/SC35-C1.rmdup.uniq.sort.bam,../4.rmdup/SC35-C2.rmdup.uniq.sort.bam,../4.rmdup/SC35-C.rmdup.uniq.sort.bam --b1 ../4.rmdup/SC35-K1.rmdup.uniq.sort.bam,../4.rmdup/SC35-K2.rmdup.uniq.sort.bam,../4.rmdup/SC35-K.rmdup.uniq.sort.bam --exon_s 1 --intron_s 1 --group-info grouping.gf

rmats2sashimiplot --l1 cKO --l2 WT -o ./Srsf2_AS_rmdup/ -t SE -e ./select_se_events.txt --b1 ../3.uniq/SC35-K1.uniq.sort.bam,../3.uniq/SC35-K2.uniq.sort.bam,../3.uniq/SC35-K.uniq.sort.bam --b2 ../3.uniq/SC35-C1.uniq.sort.bam,../3.uniq/SC35-C2.uniq.sort.bam,../3.uniq/SC35-C.uniq.sort.bam --exon_s 1 --intron_s 1 --group-info grouping.gf


rmats2sashimiplot --l1 cKO --l2 WT -o ./Srsf2_AS_mapping/ -t SE -e ./select_se_events.txt --b1 ../2.mapping/SC35-K1.sort.bam,../2.mapping/SC35-K2.sort.bam,../2.mapping/SC35-K.sort.bam --b2 ../2.mapping/SC35-C1.sort.bam,../2.mapping/SC35-C2.sort.bam,../2.mapping/SC35-C.sort.bam --exon_s 1 --intron_s 1 --group-info grouping.gf


