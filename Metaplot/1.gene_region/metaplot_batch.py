import sys
import os

path, annot = sys.argv[1:3]
cs_bed = [ path+i for i in os.listdir(path) if i.endswith(".cs.bed") ]
cs_bed.sort()

for cs in cs_bed:
    prefix = cs.split("/")[-1].split(".")[0]
    cmd = f"python3 metaplot.py {cs} {annot} >{prefix}.dist_measure.tsv"
    print(cmd)

