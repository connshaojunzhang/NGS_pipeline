import sys
import math

##
# python3 4.2-calc_coverage.py HeLa_merge.finalCluster.filter1.bedpe left_arm.txt right_arm.txt >HeLa_merge.finalCluster.filter1_coverage.bedpe
##

left = { line.strip().split('\t')[0]:line.strip().split('\t')[1] for line in open(sys.argv[2]) }
right = { line.strip().split('\t')[0]:line.strip().split('\t')[1] for line in open(sys.argv[3]) }

for line in open(sys.argv[1]):
    s = line.strip().split('\t')
    cov = int(s[7]) / math.sqrt( int(left[s[6]]) * int(right[s[6]]) )
    print(line.strip(), s[7], left[s[6]], right[s[6]], cov, sep="\t")



