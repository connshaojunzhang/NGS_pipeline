import sys

#chr1	12625	13087	RI_1	1_1

stat = {}
for line in open(sys.argv[1]):
    chrom, left, right, name, key= line.strip().split('\t')
    if key not in stat:
        stat[key]={'chrom':chrom, 'left':[int(left), int(left)+1], 'right':[int(right)-1, int(right)] , 'ri':[]}
    stat[key]['left'] = [ min(int(left), stat[key]['left'][0]), max(int(left)+1, stat[key]['left'][1])]
    stat[key]['right'] = [ min(int(right)-1, stat[key]['right'][0]), max(int(right), stat[key]['right'][1]) ]
    stat[key]['ri'].append(name)

for key in stat:
    print(stat[key]['chrom'], stat[key]['left'][0], stat[key]['left'][1], stat[key]['chrom'], stat[key]['right'][0], stat[key]['right'][1], key,  len(set(stat[key]['ri'])), '+', '+', ','.join(list(set(stat[key]['ri']))), sep="\t" )
