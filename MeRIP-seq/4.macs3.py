import sys
import os

# macs3 callpeak -t ../3.uniq/MeRIP-GV-MeRIP1.sort.uniq.bam -c ../3.uniq/MeRIP-GV-Input1.sort.uniq.bam --keep-dup all --nomodel -g mm -f BAM -q 0.05 -n MeRIP-GV-MeRIP1 --outdir MeRIP-GV-MeRIP1

path = sys.argv[1]
m6a = [ path+i for i in os.listdir(path) if i.find("m6A") >= 0 and i.find("run") < 0 and i.endswith(".sort.bam") ]
m6a.sort()
ins = [ path+i for i in os.listdir(path) if i.find("RNA") >= 0 and i.endswith(".sort.bam") ]
ins.sort()

#print(m6a)
#print(ins)

for t, c in zip(m6a, ins):
    prefix = t.split('/')[-1].split('.')[0]
    cmd = f"macs3 callpeak -t {t} -c {c} --keep-dup all --nomodel -g mm -n {prefix} --outdir {prefix}"
    print(cmd)


