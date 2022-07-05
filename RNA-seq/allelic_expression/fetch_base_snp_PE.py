# -*- coding: utf-8 -*-
"""
Created on Sat Sep  1 20:55:15 2018

@author: duzc
"""

#usage: python3 1.fetch_base_snp_PE.py ../0.snp_ref/C57_DBA_snp.bed /path/to/in.bam

import pysam
import sys

snp_dict = {}
for line in open(sys.argv[1], 'r'):
    s = line.strip().split('\t')
    loc = s[0] +":"+ s[2]
    maternal, paternal = s[3].split('|')
    if not loc in snp_dict:
        snp_dict[loc] = {'m':[], 'p':[]}
    snp_dict[loc]['m'] = list(set(maternal.split(',')))
    snp_dict[loc]['p'] = list(set(paternal.split(',')))
    #break
#print(len(snp_dict.keys()))

processed_reads = {}
samfile = pysam.AlignmentFile(sys.argv[2], 'rb')
for pileupcolumn in samfile.pileup():
    chrom = samfile.references[pileupcolumn.reference_id]
    pos = str(pileupcolumn.pos+1)
    k = chrom +":"+ pos
    if k in snp_dict.keys():
        #print(k)
        for pileupread in pileupcolumn.pileups:
            if pileupread.is_del or  pileupread.is_refskip:
                continue
            read_name = pileupread.alignment.query_name
            if not read_name in processed_reads.keys():
                processed_reads[read_name] = {'read1':[], 'read2':[]}
            read_pair = 'read1' if pileupread.alignment.is_read1 else 'read2'
            query_base = pileupread.alignment.query_sequence[pileupread.query_position]
            query_base_qual = pileupread.alignment.query_qualities[pileupread.query_position]
            if query_base_qual < 30: #filter low quality base snp
                continue
            if query_base in snp_dict[k]['m']:
                allele = 'm'
            elif query_base in snp_dict[k]['p']:
                allele = 'p'
            else:
                allele = 'b'
            processed_reads[read_name][read_pair].append([k, query_base, query_base_qual, allele])
           
            #print(read_name, k, ''.join(snp_dict[k]['m']), ''.join(snp_dict[k]['p']) , query_base, query_base_qual)
outfile = sys.argv[2].split('/')[-1].split('.')[0] + '.allelic_information'
out = open('./1.reads_allelic_information/' + outfile, 'w')

phase = {} #chrom pos ref alt bases quals
for read_name in processed_reads:
    #1.reads allelic information
    for i in processed_reads[read_name]:
        if len(processed_reads[read_name][i]) == 0:
            continue
        snps = '|'.join([ j[0] for j in processed_reads[read_name][i] ])
        bases = ''.join([ j[1] for j in processed_reads[read_name][i] ] )
        quals = ','.join([ str(j[2]) for j in processed_reads[read_name][i] ] )
        alleles = ''.join( [j[3] for j in processed_reads[read_name][i] ] )
        outline = '\t'.join( [ read_name, i, bases, quals, alleles, snps] )
        out.writelines(outline + '\n')
    #1.get snp coverage information
    read1 = processed_reads[read_name]['read1']
    read1_snps = [j[0] for j in read1]
    read1_bases = [j[1] for j in read1]
    read1_quals = [j[2] for j in read1]
    read1_alleles = [j[3] for j in read1]
    
    read2 = processed_reads[read_name]['read2']
    read2_snps = [j[0] for j in read2]
    read2_bases = [j[1] for j in read2]
    read2_quals = [j[2] for j in read2]
    read2_alleles = [j[3] for j in read2]
    
    #1.1 filter ambigous read pair
    
out.close()
        





