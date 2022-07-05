import os
data = os.listdir("../0.rawdata/")
paired=[]
for i in data:
	if i.endswith('.fq.gz'):
		paired.append(i)
if len(paired) %2 != 0:
	print('num Not Paired!!!')
	exit()
paired.sort()
for i in range(0,len(paired),2):
	file1 = paired[i]
	file2 = paired[i+1]
	#print(file1,file2)
	cmd='java -jar /home/liuzhe/Software/Trimmomatic-0.36/trimmomatic-0.36.jar PE -phred33  ../0.rawdata/%s ../0.rawdata/%s  %s.paired.fq.gz %s.unpaired.fq.gz %s.paired.fq.gz %s.unpaired.fq.gz'%(file1,file2,file1.split(".")[0],file1.split(".")[0],file2.split(".")[0],file2.split(".")[0]) + ' ILLUMINACLIP:/home/liuzhe/Software/Trimmomatic-0.36/adapters/TruSeq3-PE-2.fa:2:30:10:8:true LEADING:3 TRAILING:3 SLIDINGWINDOW:4:15 HEADCROP:10 MINLEN:36'
	print(cmd)
#	os.system(cmd)
