
#intersectBed -wa -wb -a ../1.exon_length_expr_filter/1.P0_T1.bed -b ../../0.annotation/gencode.v19.annotation.gff3 -loj |awk 'BEGIN{OFS="\t"}{if($7==".") print $1, $2, $3, $4, $5, $6}' >1.P0_T1.nonoverlap.bed
#intersectBed -wa -wb -a ../1.exon_length_expr_filter/2.P0_T2.bed -b ../../0.annotation/gencode.v19.annotation.gff3 -loj |awk 'BEGIN{OFS="\t"}{if($7==".") print $1, $2, $3, $4, $5, $6}' >2.P0_T2.nonoverlap.bed
#intersectBed -wa -wb -a ../1.exon_length_expr_filter/3.P0_T3.bed -b ../../0.annotation/gencode.v19.annotation.gff3 -loj |awk 'BEGIN{OFS="\t"}{if($7==".") print $1, $2, $3, $4, $5, $6}' >3.P0_T3.nonoverlap.bed

intersectBed -wa -wb -a ./1.P0_T1.nonoverlap.bed -b ../../0.annotation/NONCODEv5_hg19.lncAndGene.bed -loj  >1.P0_T1_NON.nonoverlap.bed
intersectBed -wa -wb -a ./2.P0_T2.nonoverlap.bed -b ../../0.annotation/NONCODEv5_hg19.lncAndGene.bed -loj >2.P0_T2_NON.nonoverlap.bed
intersectBed -wa -wb -a ./3.P0_T3.nonoverlap.bed -b ../../0.annotation/NONCODEv5_hg19.lncAndGene.bed -loj >3.P0_T3_NON.nonoverlap.bed





