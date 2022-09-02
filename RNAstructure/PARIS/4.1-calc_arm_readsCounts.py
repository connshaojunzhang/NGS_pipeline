import sys

#chr1    14695   14707   75698_74647     0       -       chr1    14625   14714   Sample1_Part_27585799   0       -
stat = {}
for line in sys.stdin:
    #print(line)
    s = line.strip().split('\t')
    if not s[3] in stat:
        stat[s[3]] = []
    stat[s[3]].append(s[9])

for key in stat:
    print(key, len(set(stat[key])), sep="\t")


