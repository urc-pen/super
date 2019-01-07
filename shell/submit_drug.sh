#!/bin/bash
#$ -S /bin/bash
#$ -cwd

for pi in `cat ../paratxt/pi2.txt`;do
for dr in `cat ../paratxt/dr.txt`;do
for ef in `cat ../paratxt/ef.txt`;do
qsub -l s_vmem=13G,mem_req=13G super_exe_drug.sh $pi $dr $ef
done
done
done
