#!/bin/bash
#$ -S /bin/bash
#$ -cwd

for i in 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27 28 29 30;do
for mt in `cat ../paratxt/mt.txt`;do
for dr in `cat ../paratxt/dr.txt`;do
for ef in `cat ../paratxt/ef.txt`;do
for we1 in `cat ../paratxt/we1.txt`;do
for we2 in `cat ../paratxt/we2.txt`;do
qsub -l s_vmem=12G,mem_req=12G super_exe_alldrug.sh $mt $dr $ef $we1 $we2
done
done
done
done
done
done
