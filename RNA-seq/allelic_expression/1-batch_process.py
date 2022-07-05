#python3 1.fetch_base_snp_PE.py ../0.snp_ref/C57_DBA_snp.bed ../1.data/Index-1cell-1.keep.sort.bam >Index-1cell-1.allelic_informiation

import os
files = ["../1.data/"+i for i in os.listdir('../1.data/') if i.endswith('.bam')]
for file in files:
    #prefix = file.split('/')[-1].split('.')[0]
    cmd = 'python3 1.fetch_base_snp_PE.py ../0.snp_ref/C57_DBA_snp.bed %s'%(file)
    print(cmd)


