import os

folders = ['../'+i for i in os.listdir('../') if i.startswith('Index')]
while len(folders) < 47:
    folders = ['../'+i for i in os.listdir('../') if i.startswith('Index')]
folders.sort()

files = []
for folder in folders:
    for file in os.listdir(folder):
        if file.endswith('_Aligned.out.bam'):
            files.append(folder +'/'+ file)
#print(len(files))

for file in files:
    prefix = file.split('/')[-1].split('_')[0]
    cmd = r'samtools view -h %s |grep -E "^@|\bNH:i:1\b" |samtools sort -o ./%s.uniq.sort.bam'%(file, prefix)
    print(cmd)

