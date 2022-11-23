#python3 1.create_exon_bed.py ./target.psi

bedtools coverage -a left_exon.bed -b molecular_cell.bed -nobuf -F 0.5 -counts > left_exon.tab
bedtools coverage -a left_intron.bed -b molecular_cell.bed -nobuf -F 0.5 -counts > left_intron.tab
bedtools coverage -a mid_exon.bed -b molecular_cell.bed -nobuf -F 0.5 -counts > mid_exon.tab
bedtools coverage -a right_intron.bed -b molecular_cell.bed -nobuf -F 0.5 -counts > right_intron.tab

python3 2.stat.py left_exon.tab >left_exon.list
python3 2.stat.py left_intron.tab >left_intron.list
python3 2.stat.py mid_exon.tab >mid_exon.list
python3 2.stat.py right_intron.tab >right_intron.list

python3 3.paste.py >merge_irCLIP.xls

python3 4.1-tab_file_sum_nega.py ./merge_irCLIP.xls >neg.avg.xls
python3 4.2-tab_file_sum_posi.py merge_irCLIP.xls >pos.avg.xls

paste neg.avg.xls pos.avg.xls > avg_molecular_cell.xls



