import sys

stat = {}
for line in open(sys.argv[1], 'r'):
    chrom, start, end, infor, col5, strand, depth = line.strip().split('\t')
    event, win, flag = infor.split('_')
    if flag == 'bad':
        depth = 0
    if not int(event) in stat.keys():
        stat[int(event)] = {}
    stat[int(event)][int(win)] = int(depth)

print('windows')
for i in sorted(stat):
    outline = str(i) +'\t'+ '\t'.join( [ str(stat[i][j]) for j in sorted(stat[i])])
    print(outline)
