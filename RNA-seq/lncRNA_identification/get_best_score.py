# -*- coding: utf-8 -*-
"""
Created on Fri Mar 30 22:02:19 2018

@author: pc
"""

import os
files = [i for i in os.listdir() if i.endswith('_window.tab')]

for file in files:
    prefix = file.split('_window.tab')[0]
    
    stat = {} #id:[]score, start
    for line in open(file, 'r'):
        s = line.strip().split('\t')
        key, loc = s[0].split('.')
        if not key in stat.keys():
            stat[key] = []
        stat[key].append([float(s[4]), float(s[3])])
    
    out = open(prefix+'_phastCons.tab', 'w')
    for key in stat:
        stat[key].sort()
        outline = key +'\t200\t200\t'+ str(stat[key][-1][-1]) +'\t'+ str(stat[key][-1][0]) +'\t'+ str(stat[key][-1][0])
        out.writelines(outline + '\n')
    out.close()
    
    #break
        

