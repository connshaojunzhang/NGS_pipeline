import sys
import os

#multiIntersectBed -i ./*/*.narrowPeak |grep "1,2,3" |cut -f1,2,3 >late-2cell-m6A.3sampleOverlapBase.bed
#cat ./*/*.narrowPeak |sortBed |mergeBed >late-2cell-m6A.3sampleMergedPeak.bed
#bedtools intersect -u -a ./late-2cell-m6A.3sampleMergedPeak.bed -b ./late-2cell-m6A.3sampleOverlapBase.bed >late-2cell-m6A.3sampleOverlapPeak.bed
#less -S mm9_refseq.gtf |grep -w "exon" |sortBed |mergeBed -s >exon_region.bed
#cat ./*/*.narrowPeak |awk 'BEGIN{OFS="\t"}{if($7>4) print $1, $2+$10-50, $2+$10+50}' |sortBed |mergeBed |bedtools intersect -u -a - -b ./late-2cell-m6A.3sampleOverlapPeak.bed |sortBed >late-2cell-m6A.consensusSummit.be


summits, exons = sys.argv[1:3]
cmd = rf"""bedtools intersect -a {summits} -b {exons} -wo """

stat = {}
for line in os.popen(cmd).read().strip().split("\n"):
    chrom, start, end, _, _, _, strand, _ = line.strip().split("\t")
    key = "\t".join([chrom, start, end])
    if not key in stat:
        stat[key] = set()
    stat[key].add(strand)

k = 1
for key in stat:
    if len(stat[key]) == 1:
        print(key, f"exon_peak_{k}", 0, list(stat[key])[0], sep="\t")
        k += 1


