import sys
import gzip

trim, unpair, merge = sys.argv[1:4]
tr_dict = {'A':'T', 'C':'G', 'G':'C', 'T':'A', 'N':'N'}
trim_len = 2

for line in gzip.open(trim, "rt"):
    if line[0] == "@":
        s = line.strip().split(' ')[0]
        outline = s[:-10] + '_' + ''.join(s[-9:].split('_'))
    else:
        outline = line.strip()
        if outline != "+":
            outline = outline[trim_len:]
    print(outline)

for line in gzip.open(unpair, "rt"):
    if line[0] == "@":
        s = line.strip().split(' ')[0]
        outline = s[:-10] + '_' + ''.join(s[-9:].split('_'))
    else:
        outline = line.strip()
        if outline != "+":
            outline = outline[trim_len:]
    print(outline)

merge_file = gzip.open(merge, "rt")
for line1 in merge_file:
    s = line1.strip().split(' ')[0]
    name = s[:-10] + '_' + ''.join(s[-9:].split('_'))
    seq = ''.join([ tr_dict[base] for base in merge_file.readline().strip().upper()[-trim_len-1::-1] ])
    line3 = merge_file.readline().strip()
    qual = merge_file.readline().strip()[-trim_len-1::-1]
    print(name, seq, line3, qual, sep="\n")
merge_file.close()
