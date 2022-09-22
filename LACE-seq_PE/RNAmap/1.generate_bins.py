import sys

diff_thr, fdr_thr = 0.05, 0.001
on_exon, on_intron, bs = 100, 400, 10
for n, line in enumerate(open(sys.argv[1])):
    if n == 0:
        colnames = line.strip().split("\t")
        continue

    se_info = dict(zip(colnames, line.strip().split("\t")))
    fdr, diff = float(se_info["FDR"]), float(se_info["IncLevelDifference"])
    if fdr < fdr_thr and diff > diff_thr:
        group = "Inclusion"
    elif fdr < fdr_thr and diff < -diff_thr:
        group = "Skip"
    else:
        continue
    
    chrom, strand = se_info["chr"], se_info["strand"]
    gene_id, symbol = se_info["ID"], se_info["geneSymbol"][1:-1]

    up_exon = [int(se_info["upstreamES"]), int(se_info["upstreamEE"])]
    mid_exon = [int(se_info["exonStart_0base"]), int(se_info["exonEnd"])]
    down_exon = [int(se_info["downstreamES"]), int(se_info["downstreamEE"])]
    up_intron = [up_exon[1], mid_exon[0]]
    down_intron = [mid_exon[1], down_exon[0]]

    config = [ [up_exon[1]-on_exon, up_exon[1]+on_intron, up_exon[0], sum(up_intron)//2, "up_e0"],
               [mid_exon[0]-on_intron, mid_exon[0]+on_exon, sum(up_intron)//2, sum(mid_exon)//2, "up_e1"],
               [mid_exon[1]-on_exon, mid_exon[1]+on_intron, sum(mid_exon)//2, sum(down_intron)//2, "down_e0"],
               [down_exon[0]-on_intron, down_exon[0]+on_exon, sum(down_intron)//2, down_exon[1], "down_e1"] ]
    
    for s, e, s_bd, e_bd, key in config:
        for i, bin_s in enumerate(range(s, e, bs)):
            is_use = 1 if (bin_s>=s_bd and bin_s<=e_bd) else 0
            print(chrom, bin_s, bin_s+bs, f"{gene_id}|{group}|{symbol}|{key}_{i}|{is_use}", 0, strand, sep="\t")


