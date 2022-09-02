import sys

def calc_overlap_distance(core_region_left, core_region_right, cur_region_left, cur_region_right, min_overlap=5):
    overlap_left = core_region_left[-1] - cur_region_left[0]
    if overlap_left < min_overlap:
        return False, None, None
    elif (core_region_right[-1] - cur_region_right[0]) < min_overlap or (core_region_right[0] - cur_region_right[-1]) > -min_overlap:
        return False, None, None
    else:
        new_core_left = [ max(core_region_left[0], cur_region_left[0]), min(core_region_left[-1], cur_region_left[-1]) ]
        new_core_right = [ max(core_region_right[0], cur_region_right[0]), min(core_region_right[-1], cur_region_right[-1]) ]
        return True, new_core_left, new_core_right

def split_clusters(tmp):
    core_region = []
    for line in tmp:
        s = chrom1, start1, end1, chrom2, start2, end2, name, score, strand1, strand2, reads = line
        s[1:3] = int(start1), int(end1)
        s[4:6] = int(start2), int(end2)
        if core_region == []:
            core_region.append(s)
        else:
            core_region_left = [int(core_region[-1][1]), int(core_region[-1][2])]
            core_region_right = [int(core_region[-1][4]), int(core_region[-1][5])]
            cur_region_left = [int(s[1]), int(s[2])]
            cur_region_right = [int(s[4]), int(s[5])]
            flag, new_core_left, new_core_right = calc_overlap_distance(core_region_left, core_region_right, cur_region_left, cur_region_right)
            if flag:
                core_region[-1][1:3] = new_core_left
                core_region[-1][4:6] = new_core_right
                core_region[-1][-1].extend( reads )
            else:
                core_region.append(s)
    core_region.sort()
    return core_region

    
orignal_clusters = {}
for line in open(sys.argv[1]):
    s = line.strip().split('\t')
    if not s[-1] in orignal_clusters:
        orignal_clusters[s[-1]] = []
    orignal_clusters[s[-1]].append(s[:-1])
    orignal_clusters[s[-1]][-1].append([s[6]])

for key in orignal_clusters:
    tmp = orignal_clusters[key]
    tmp.sort()
    if len(tmp) == 1:
        print('\t'.join(map(str, tmp[0][:6])), key, 1, '\t'.join(map(str, tmp[0][8:-1])), ','.join(tmp[0][-1]), sep="\t" )
        pass
    else:
        cur_clusters = split_clusters(tmp)
        num = len(cur_clusters)
        #print(key, num)
        while True:
            cur_clusters = split_clusters(cur_clusters)
            cur_num = len(cur_clusters)
            if cur_num < num:
                num = cur_num
            else:
                break
        #print(cur_clusters)
        if len(cur_clusters) == 1:
            tmp = cur_clusters
            print('\t'.join(map(str, tmp[0][:6])), key, len(tmp[0][-1]), '\t'.join(map(str, tmp[0][8:-1])), ','.join(tmp[0][-1]), sep="\t" )
        else:
            for n, line in enumerate(cur_clusters):
                print('\t'.join(map(str, line[:6])), key+".%d"%(n+1), len(line[-1]), '\t'.join(map(str, line[8:-1])), ','.join(line[-1]), sep="\t" )

           
       


