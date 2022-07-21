import sys
import pandas as pd
import numpy as np


def parse_attrs(attrs):
    tmp = {}
    for i in attrs.replace('"', '').split(";")[:-1]:
        key, val = i.strip().split(" ")
        tmp[key] = val
    return tmp["transcript_id"], tmp["gene_name"]

## 0. parse   
gtf = sys.argv[1]

## 1. stat transcript
trans_summary = {}
for line in open(gtf):
    if line.startswith("#"):
        continue
    
    chrom, _m, feature, start, end, _, strand, _, attrs = line.strip().split("\t")
    if feature == "gene":
        continue
    trans_id, gene_name = parse_attrs(attrs)

    if not trans_id in trans_summary:
        trans_summary[trans_id] = {"region":[]}
    if feature == "transcript":
        trans_summary[trans_id].update({'chr':chrom, 'st':int(start), 'ed':int(end), "strand":strand, "gn":gene_name})
    else:
        trans_summary[trans_id]["region"].append([int(start), int(end), feature])

#print(len(trans_summary))
n2f = {1:'CDS', 2:'UTR'}
f2n = {'start_codon':1, 'CDS':1, 'UTR':2, 'stop_codon':1, 'exon':1}
for trans_id in trans_summary:

    # 0.parse
    chrom = trans_summary[trans_id]["chr"]
    st, ed = trans_summary[trans_id]["st"], trans_summary[trans_id]['ed']
    strand = trans_summary[trans_id]['strand']
    gn = trans_summary[trans_id]["gn"]
    region = trans_summary[trans_id]["region"]
 
    # 1.trans_full
    trans_full = pd.Series(np.zeros(ed-st+1, dtype=int))
    trans_full.index = np.arange(st, ed+1)
    for s, e, f in region:
        if f in f2n:
            trans_full[np.arange(s, e+1)] = f2n[f]

    # 2.trans_collapse
    trans_collapse = [ [trans_full[st], st, st] ]
    for val in trans_full.values[1:]:
        if val == trans_collapse[-1][0]:
            trans_collapse[-1][2] += 1
        else:
            last_end = trans_collapse[-1][2]
            trans_collapse.append([ val, last_end+1, last_end+1])
    trans_collapse = [ [n2f[r[0]], r[1], r[2]] for r in trans_collapse if r[0] != 0 ]
    if strand == "-":
        trans_collapse = trans_collapse[::-1]

    # 3.seperate 5'UTR and 3'UTR 
    curr_feat = [ trans_collapse[0][0] ]
    trans_group = [ [trans_collapse[0].copy()] ]
    for r in trans_collapse[1:]:
        if r[0] == curr_feat[-1]:
            trans_group[-1].append(r.copy())
        else:
            trans_group.append([r.copy()])
            curr_feat.append(r[0])
    if len(curr_feat) != 1:
        if curr_feat[0] == "UTR":
            curr_feat[0] = "UTR5"
        if curr_feat[-1] == "UTR":
            curr_feat[-1] = "UTR3"
    
    for feat, group in zip(curr_feat, trans_group):
        feature_size = [ r[2]-r[1]+1 for r in group ]
        icmt = str(1/sum(feature_size))
        relative_pos = np.cumsum(feature_size)
        relative_pos = [0] + (relative_pos/relative_pos[-1]).tolist()
        for i, r in enumerate(group):
            feat_id = "|".join([gn, trans_id, feat, str(i), icmt])
            print(chrom, r[1]-1, r[2], feat_id, relative_pos[i], strand, sep="\t")

