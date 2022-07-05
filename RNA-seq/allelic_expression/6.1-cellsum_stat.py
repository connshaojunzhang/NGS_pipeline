import os

index = {'A':0, 'C':1, 'G':2, 'T':3}

alleles = {} #alleles[chrom:pos] = (ref, alt)
with open('/mnt/pub/work/duzc/p1.early-embryo_srb/0.ref/1.snp_annotation/DBAsnps_alleles.vcf', 'r') as infile:
    for line in infile:
        if line[0] == '#':
            continue
        s = line.strip().split('\t')
        if s[4].count(',') >= 1:
            continue
        key = 'chr'+ s[0] +':'+ s[1]
        if key not in alleles:
            alleles[key] = (s[3], s[4])

files = [ '../0.cellsums/'+i for i in os.listdir('../0.cellsums') if i.endswith('.cellsum')]
for file in files:
    prefix = file.split('/')[-1].split('.')[0]
    print(prefix)
    out = open(prefix + '.stat', 'w')
    for line in open(file):
        s = line.strip().split('\t')
        key = s[0] +":"+ s[1]
        if (s[0] == 'chrX') or (not key in alleles.keys()) :
            continue
        read = s[2:]
        ref_read = read[index[alleles[key][0]]]
        alt_read = read[index[alleles[key][1]]]
        all_read = int(ref_read) + int(alt_read)
        if all_read == 0:
            continue
        ref_ratio = int(ref_read) / all_read
        alt_ratio = int(alt_read) / all_read
        out.writelines( '\t'.join([s[0], s[1], alleles[key][0], alleles[key][1], ref_read, alt_read, str(all_read), str(ref_ratio), str(alt_ratio)]) + '\n' )

    out.close()




