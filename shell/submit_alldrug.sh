#!/bin/bash
#$ -S /bin/bash
#$ -cwd

for mt in `cat ../paratxt/mt.txt`;do
for dr in `cat ../paratxt/dr.txt`;do
for ef in `cat ../paratxt/ef.txt`;do
for we1 in `cat ../paratxt/we1.txt`;do
for we2 in `cat ../paratxt/we2.txt`;do
qsub -l s_vmem=9G,mem_req=9G super_exe_alldrug.sh $mt $dr $ef $we1 $we2
done
done
done
done
done
