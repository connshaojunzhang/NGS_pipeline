import sys

import regex
import gzip

def readm(file_obj, n):
    i, lines = 0, []
    for line in file_obj:
        i += 1
        lines.append(line.strip())
        if i >= n:
            yield lines
            i = 0
            lines.clear()
    if i > 0:
        yield lines

files = sys.argv[1:]
tr_dict = {'A':'T', 'C':'G', 'G':'C', 'T':'A', 'N':'N'}
umi_len, min_len = 18, 18

for i, f in enumerate(files):
    for head, seq, _, qual in readm(gzip.open(f, "rt"), 4):
        # 1. preprocessing
        head = head.split()[0]
        head, umi1 = head[:-5], head[-4:]
        if i == 0:
            seq = "".join([ tr_dict[i] for i in seq.upper()[::-1] ])
            qual = qual[::-1]
        else:
            seq = seq.upper()
        
        # 2. fetch UMI sequence in reads 2
        tmp = regex.search("(CAATCG){i<=1,d<=1,s<=1,3i+3d+2s<=3}", seq[:18], flags=regex.BESTMATCH )
        if tmp is None or tmp.span()[0] > 8:
            continue
        loc = tmp.span()
        end = loc[1]+8
        if loc[0] < 4:
            umi2 = "N" * (4-loc[0]) + seq[:loc[0]] + seq[loc[1]:end]
        else:
            umi2 = seq[loc[0]-4:loc[0]] + seq[loc[1]:end]
        seq = seq[end:]
        qual = qual[end:]
         
        # 3. output
        if len(seq) >= min_len:
            print("\n".join([head+"_"+umi1+umi2, seq, "+", qual]))



