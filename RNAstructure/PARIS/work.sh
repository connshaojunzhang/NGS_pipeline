##
# 0. preprocessing
##
#less -S ../3.Paris_workflow_v2/HeLa_merge.C4.intragene.Chimeric.igv.withID.bed |awk 'BEGIN{OFS="\t"}{if($0!~/track/) print $1, $2, $3}' |sort -k1,1V -k2,2n |uniq |awk 'BEGIN{OFS="\t"}{print $1, $2, $2+1, "RI_"NR, $3}' |bedtools cluster -d 10 |awk 'BEGIN{OFS="\t"}{print $1, $5-1, $5, $4, $2, $6}' |sortBed |bedtools cluster -d 10 |awk 'BEGIN{OFS="\t"}{print $1, $5, $3, $4, $6"_"$7}' >HeLa_merge.C4.intragene.Chimeric.sort.uniq.bed
#less -S HeLa_merge.C4.intragene.Chimeric.sort.uniq.bed |awk 'BEGIN{OFS="\t"}{print $1, $2, $2+1, $4, 0, "+\n"$1, $3-1, $3, $4, 0, "+"}' >test.bed
#python3 0.merge_RI.py HeLa_merge.C4.intragene.Chimeric.sort.uniq.bed >HeLa_merge.C4.intragene.Chimeric.sort.uniq.bedpe

##
# 2. finalCluster
##
#chr1	17938	17987	chr1	17938	17993	1_1	1	+	+	Sample1_ChimericWhole_32558020
#less -S HeLa_merge.C4.intragene.Chimeric.sort.uniq.bedpe |awk 'BEGIN{OFS="\t"}{if($9==$10)print $1, $2, $3, $7, $8, $9, $5, $6, $10, $11}' |sortBed |bedtools cluster -s -d 10 |awk 'BEGIN{OFS="\t"}{print $1, $7, $8, $4, $5, $9, $2, $3, $6, $10, $11}' |sortBed |bedtools cluster -s -d 10 |awk 'BEGIN{OFS="\t"}{print $1, $7, $8, $1, $2, $3, $4, $5, $9, $6, $10, $11"_"$12}' >HeLa_merge.originalCluster2.bedpe
#python3 2.merge_cluster.py HeLa_merge.originalCluster2.bedpe >HeLa_merge.finalCluster.bedpe


##
# 3. filter
##
#less -S HeLa_merge.finalCluster.bedpe |awk '{if($8>2 && ($3<$5)) print $0}' >HeLa_merge.finalCluster.filter1.bedpe
#less -S HeLa_merge.finalCluster.filter1.bedpe |awk 'BEGIN{OFS="\t"}{print $1, $2, $3, $7, 0, $9}' |sortBed |bedtools intersect -s -a - -b test.bed -wa -wb |python3 4.1-calc_arm_readsCounts.py >left_arm.txt
#less -S HeLa_merge.finalCluster.filter1.bedpe |awk 'BEGIN{OFS="\t"}{print $1, $5, $6, $7, 0, $9}' |sortBed |bedtools intersect -s -a - -b test.bed -wa -wb |python3 4.1-calc_arm_readsCounts.py >right_arm.txt
#python3 4.2-calc_coverage.py HeLa_merge.finalCluster.filter1.bedpe left_arm.txt right_arm.txt >HeLa_merge.finalCluster.filter1_coverage.bedpe
#less -S HeLa_merge.finalCluster.filter1_coverage.bedpe |awk '{if($NF>0.01) print $0}' >HeLa_merge.finalCluster.filter2.bedpe


##
# 4. select
##
#python3 5.select_RI.py HeLa_merge.finalCluster.filter2.bedpe test.bed
#less -S HeLa_merge.finalCluster.filter2.bedpe |awk 'BEGIN{OFS="\t"}{print $1, $2, $3, $7"_1", $8, $9"\n"$4, $5, $6, $7"_2", $8, $10}' >HeLa_merge.select_cluster.bed


##
# 5. psudoknots
##
#less -S HeLa_merge.finalCluster.filter2.bedpe |awk 'BEGIN{OFS="\t"}{print $1, $2, $6, $7, $8, $9, $2, $3, $5, $6}' >HeLa_merge.gapped_region.bed
#less -S HeLa_merge.finalCluster.filter2.bedpe |awk 'BEGIN{OFS="\t"}{print $1, $2, $6, $7, $8, $9, $2, $3, $5, $6}' | bedtools intersect -a - -b HeLa_merge.gapped_region.bed -wa -wb |awk '{if($4!=$14) print $0}'>psudoknots.txt
python3 7.filter_psudoknots.py psudoknots.txt 100 2 >psudoknots.final.txt



