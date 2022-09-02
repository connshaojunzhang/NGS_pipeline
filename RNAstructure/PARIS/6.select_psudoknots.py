import sys

#chr1	566748	566783	23_18	2	+	566748	566762	566765	566783	chr1	566748	566783	23_18	2	+	566748	566762	566765	566783

stat = {}
for line in sys.stdin:
    s = line.strip().split('\t')
    cluster1_left = [int(s[6]), int(s[7])]
    cluster1_right = [int(s[8]), int(s[9])]
    cluster2_left = [int(s[16]), int(s[17])]
    cluster2_right = [int(s[18]), int(s[19])]
    if s[3] == s[13]:
        continue
    if (cluster2_left[1] < cluster1_right[0] and cluster1_right[1] < cluster2_right[0]) and (cluster1_left[1] < cluster2_left[0] and cluster2_left[1]< cluster1_right[0]):
        key = [s[3], s[13]]
    elif (cluster2_left[1] < cluster1_left[0] and cluster1_left[1] < cluster2_right[0]) and (cluster1_left[1] < cluster2_right[0] and cluster2_right[1] < cluster1_right[0]):
        key = [s[3], s[13]]
    else:
        continue
    key.sort()
    key = ','.join(key)
    if not key in stat:
        stat[key] = line.strip()

for key in stat:
    print(stat[key])

