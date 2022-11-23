import os

files = [ i for i in os.listdir() if i.endswith('.list') ]
files.sort()

stat = {}
for i in ['left_exon.list', 'left_intron.list', 'mid_exon.list', 'right_intron.list']:
    prefix = i.split('.')[0]
    stat[i] = {}
    for line in open(i, 'r'):
        s = line.strip().split('\t')
        if not s[0] in stat.keys():
            stat[s[0]] = ''
        stat[s[0]] += '\t'.join(s[1:]) +'\t'

row_num = 0
for line in open('target.psi', 'r'):
    if line.startswith('ID'):
        print(line.strip())
        continue
    row_num += 1
    if str(row_num) in stat.keys():
        print(line.strip() + '\t' + stat[str(row_num)][:-1])
    else:
        print(line.strip() +'\tintron_too_short')

