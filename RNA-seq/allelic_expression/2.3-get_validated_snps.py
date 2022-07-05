# -*- coding: utf-8 -*-
"""
Created on Sat Mar 10 10:23:28 2018

@author: pc
"""

nts = {'A':4, 'C':5, 'G':6, 'T':7, 'N':8 }

fout = open('validated_dba_c57_snps.txt', 'w')
fout1 = open('total_dba_c57_snps.txt', 'w')

with open('snpstat_C57_DBA.txt', 'r') as dba_c57, open('snpstat_C57_pure.txt') as c57: 
    for c57_line, dba_c57_line in zip(c57, dba_c57):
        if c57_line[0] == '#':
            continue
        c57_s = c57_line.strip().split('\t')
        dba_c57_s = dba_c57_line.strip().split('\t')
        
        c57_nt, dba_nt = c57_s[2:4]
        
        c57_pos = []
        for c57n in c57_nt.split(','):
            c57_pos.append(nts[c57n])
        dba_pos = []
        for dban in dba_nt.split(','):
            dba_pos.append(nts[dban])
        
        # criteria 
        # > 90% correct genotype in pure cells
        # or !!!
        # at least 10% of each genotype in mixed cells

        #c57_pure
        if sum(map(float, c57_s[4:8])) > 0:
            c57_reads_in_c57 = sum(float(c57_s[c57p]) for c57p in c57_pos ) / sum(map(float, c57_s[4:8]))
        else:
            c57_reads_in_c57 = -1
        #dba_c57
        if sum(map(float, dba_c57_s[4:8])) > 0:
            c57_reads_in_mix = sum(float(dba_c57_s[c57p]) for c57p in c57_pos) / sum(map(float, dba_c57_s[4:8]))
            dba_reads_in_mix = sum(float(dba_c57_s[dbap]) for dbap in dba_pos) / sum(map(float, dba_c57_s[4:8]))
        else:
            c57_reads_in_mix, dba_reads_in_mix = -1, -1
        
        if c57_reads_in_c57 > 0.9 or  min(c57_reads_in_mix, dba_reads_in_mix) > 0.1:
            fout.write("\t".join(c57_s[:4]) +"\t1\t"+ "\t".join(map(str, [c57_reads_in_c57, c57_reads_in_mix, dba_reads_in_mix])) +'\n')
        if sum([c57_reads_in_c57, c57_reads_in_mix, dba_reads_in_mix]) != -3:
            fout1.write("\t".join(c57_s[:4]) +"\t1\t"+ "\t".join(map(str, [c57_reads_in_c57, c57_reads_in_mix, dba_reads_in_mix])) +'\n')
fout.close()
fout1.close()



