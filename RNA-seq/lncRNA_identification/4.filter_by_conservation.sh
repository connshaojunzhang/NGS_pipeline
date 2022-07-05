
bigWigAverageOverBed ../0.phyloP/phyloP46way.bw ./1.P0_T1.filter.bed ./1.P0_T1.filter.tab
bigWigAverageOverBed ../0.phastCons/phastCons46way.bw ./0.sort_data/1.P0_T1_window.bed ./1.P0_T1_window.tab
python3 get_best_score.py




