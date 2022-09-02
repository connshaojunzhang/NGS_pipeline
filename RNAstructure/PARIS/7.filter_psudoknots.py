import sys
import os

#chr1	17463	17560	28_29	3	+	17463	17471	17558	17560	chr1	17463	17560	28_29	3	+	17463	17471	17558	17560

cmd = r"""less -S %s |awk '{print $4}' |sort |uniq -c |awk '{if($1==1) print $2}' """%(sys.argv[1])
left_uniq = os.popen(cmd).read().strip().split('\n')
cmd = r"""less -S %s |awk '{print $14}' |sort |uniq -c |awk '{if($1==1) print $2}' """%(sys.argv[1])
right_uniq = os.popen(cmd).read().strip().split('\n')

#print(left_uniq)
#print(right_uniq)

width = int(sys.argv[2])
r = int(sys.argv[3])

stat = []
for line in open(sys.argv[1]):
    s = line.strip().split('\t')
    if s[3] in left_uniq and s[13] in right_uniq and (int(s[2])-int(s[1])) < width and (int(s[12])-int(s[11])) < width and int(s[4]) > r and int(s[14]) > r:
        key = [s[3], s[13]]
    else:
        continue
    cluster1_left = [int(s[6]), int(s[7])]
    cluster1_right = [int(s[8]), int(s[9])]
    cluster2_left = [int(s[16]), int(s[17])]
    cluster2_right = [int(s[18]), int(s[19])]
    if (cluster2_left[1] < cluster1_right[0] and cluster1_right[1] < cluster2_right[0]) and (cluster1_left[1] < cluster2_left[0] and cluster2_left[1]< cluster1_right[0]):
        key = [s[3], s[13]]
    elif (cluster2_left[1] < cluster1_left[0] and cluster1_left[1] < cluster2_right[0]) and (cluster1_left[1] < cluster2_right[0] and cluster2_right[1] < cluster1_right[0]):
        key = [s[3], s[13]]
    else:
        continue
    key.sort()
    key = '\t'.join(key)
    if key not in stat:
        stat.append(key)

for key in stat:
    print(key)
