import sys

bin_num = 50
exon_stream = 500
intron_stream = 2000

out1 = open('left_exon.bed', 'w')
out2 = open('left_intron.bed', 'w')
out3 = open('mid_exon.bed', 'w')
out4 = open('right_intron.bed', 'w')

row_num = 0
for line in open(sys.argv[1], 'r'):
    if line.startswith('ID'):
        continue
    s = line.strip().split('\t')
    chrom, strand = s[3], s[4]
    row_num += 1
    #up_start, up_end, start, end, down_start, down_end
    locs = list(map(int, s[7:9] + s[5:7] + s[9:11]))
    #l_e_len, l_i_len, e_len, r_i_len, r_e_len 
    lens = [ locs[i] - locs[i-1] + 1 for i in range(1, len(locs)) ]
    lens[1], lens[3] = lens[1] - 2, lens[3] - 2
    
    for i, j in zip( range(1, len(lens)), locs[1:5] ):# length, point
        min_start = j - lens[i-1] / 2
        max_end = j + lens[i] / 2
        #print(min_start, max_end)
        if i % 2 == 1:
            region_start = j - exon_stream
            region_end = j + intron_stream
        else:
            region_start = j - intron_stream
            region_end = j + exon_stream
        bin_len = int( (region_end - region_start + 1) / bin_num )
        region = []
        for k in range(bin_num):
            temp_start, temp_end = region_start + k*bin_len, region_start + (k+1)*bin_len - 1
            if temp_start < min_start or temp_end >max_end:
                region.append( '\t'.join(map(str, [chrom, temp_start-1, temp_end, str(row_num)+'_'+str(k)+'_bad', "0", strand])) + '\n' )
            else:
                region.append( '\t'.join(map(str, [chrom, temp_start-1, temp_end, str(row_num)+'_'+str(k)+'_good', "0", strand])) + '\n' )
        if i == 1:
            out1.writelines(region)
        elif i == 2:
            out2.writelines(region)
        elif i == 3:
            out3.writelines(region)
        elif i == 4:
            out4.writelines(region)
    #print(locs)
    #print(lens)
    #break
out1.close()
out2.close()
out3.close()
out4.close()

