########################
# uaRNA
########################
echo ">uaRNA"
bedtools intersect -s -a ${1} -b ./0.ref/gencode.v19.annotation.filter.UaRNA.sort.uniq.bed -u |awk 'BEGIN{OFS="\t"}{print $0"\tUaRNA"}' >peaks.uaRNA.bed
#1.1 genelist
python3 1.1-get_genelist.py ./0.ref/gencode.v19.annotation.filter.add_length.bed ./0.ref/gencode.v19.annotation.filter.UaRNA.sort.uniq.bed >uaRNA.genelist
#1.2 check
wc -l uaRNA.genelist
grep -E "POU3F2|POU4F2|DLX3|NEUROG2|SOX11" uaRNA.genelist

########################
# Genebody
########################
echo ">Genebody"
bedtools intersect -s -a ${2} -b ./0.ref/gencode.v19.trans_region.filter.bed -f 1 -wa -wb |awk -F '[_]|[\t]' 'BEGIN{OFS="\t"}{if($0~/Intron/) print $1, $2, $3, $4"_"$5, $6, $7, "Intron"; else print $1, $2, $3, $4"_"$5, $6, $7, $11}' |sortBed |uniq >peaks.genebody.bed
bedtools intersect -s -a ./0.ref/gencode.v19.annotation.filter.add_length.bed -b ./peaks.genebody.bed -u >genebody.genelist
less -S peaks.genebody.bed |awk '{print $NF}' |sort |uniq -c
less -S peaks.genebody.bed |awk 'BEGIN{OFS="\t"}{if($6=="+") print $1, $2, $3+30, $4, $5, $6, $7; else print $1, $2-30, $3, $4, $5, $6, $7, sep="\t"}' >peaks.genebody.bed2

########################
# Motif Enrichment
########################
echo ">Motif Enrichment"
cat ./peaks.uaRNA.bed peaks.genebody.bed2 |awk 'BEGIN{OFS="\t"}{center=int(($2+$3)/2); print $1, center-25, center+25, $4"_"$7, $5, $6}' |sortBed >peaks.region_50bp.bed
python3 3.1-calc_peak_region_kmer.py peaks.region_50bp.bed
python3 3.2-calc_enrichment.py bg.txt 3UTR.txt |sort -k2,2nr >3UTR.enrichment
python3 3.2-calc_enrichment.py bg.txt 5UTR.txt |sort -k2,2nr >5UTR.enrichment
python3 3.2-calc_enrichment.py bg.txt Intron.txt |sort -k2,2nr >Intron.enrichment
python3 3.2-calc_enrichment_v2.py bg.1 UaRNA.txt |sort -k2,2nr >UaRNA.enrichment
less -S 3UTR.enrichment |head -20 |awk '{print ">"NR"\n"$1}' >3UTR.fasta
less -S 5UTR.enrichment |head -20 |awk '{print ">"NR"\n"$1}' >5UTR.fasta
less -S Intron.enrichment |head -20 |awk '{print ">"NR"\n"$1}' >Intron.fasta
less -S UaRNA.enrichment |head -20 |awk '{print ">"NR"\n"$1}' >UaRNA.fasta
python3 3.3-get_top_N_kmer_enrichment_matrix.py 10 |sort -k5,5nr >top10.matrix
python3 3.3-get_top_N_kmer_enrichment_matrix.py 20 |sort -k5,5nr >top20.matrix

