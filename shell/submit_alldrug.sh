#!/bin/bash
#$ -S /bin/bash
#$ -cwd

for mt in `cat ../paratxt/mt.txt`;do
for dr in `cat ../paratxt/dr.txt`;do
for ef in `cat ../paratxt/ef.txt`;do
qsub -l s_vmem=12G,mem_req=12G super_exe_alldrug.sh $mt $dr $ef
done
done
done
