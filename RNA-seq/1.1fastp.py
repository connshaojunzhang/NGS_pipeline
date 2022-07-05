import os

#fastp -i ../0.rawdata/Srsf1-C1_R1.fq.gz -I ../0.rawdata/Srsf1-C1_R2.fq.gz -o ./Srsf1-C1_R1.clean.fq.gz -O ./Srsf1-C1_R2.clean.fq.gz -z 4 -g -x -q 20 -l 36 -y -c -u 40 -n 4

path = "../0.rawdata/"
f1 = [path+i for i in os.listdir(path) if i.endswith("R1.fq.gz") ]
f1.sort()
f2 = [path+i for i in os.listdir(path) if i.endswith("R2.fq.gz") ]
f2.sort()

for i, j in zip(f1, f2):
    prefix1 = i.split('/')[-1].split('.')[0]
    prefix2 = j.split('/')[-1].split('.')[0]

    cmd = f"fastp -i {i} -I {j} -o {prefix1}.clean.fq.gz -O {prefix2}.clean.fq.gz -z 4 -g -x -q 20 -l 36 -y -c -u 40 -n 4 --detect_adapter_for_pe -w 8"
    print(cmd)

