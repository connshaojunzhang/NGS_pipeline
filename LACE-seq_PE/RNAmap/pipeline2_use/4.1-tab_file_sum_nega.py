import sys

bin_num = 50
cutoff = 0.05
row_num = 0
total = [0] * 200
complexity = [0] * 200

for line in open(sys.argv[1], 'r'):
    if line.find('intron_too_short') >= 0 or line.startswith('ID'):
        continue
    s = line.strip().split('\t')
    if float(s[19]) > 1 or (not s[0].startswith('-')):
        continue
    tmp = list(map(float, s[23:]))
    if s[4] == '-':
        tmp.reverse()
    sum_tmp = sum(map(float, tmp))
    if sum_tmp < cutoff:
        continue
    else:
        row_num += 1
        for i in range(len(tmp)):
            total[i] += tmp[i] / sum_tmp
            if tmp[i] > 2:
                complexity[i] += 1

print('event: ', row_num)
i, j = 0, 0
for k in range(len(total)):
    i += 1
    j += 1
    tmp = total[k] / row_num * complexity[k]/row_num
    print(j, tmp)
    if (i % bin_num) == 0:
        for l in range(10):
            j += 1
            print(j, 0)

