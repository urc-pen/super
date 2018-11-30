#!/bin/bash
#$ -S /bin/bash
#$ -cwd
for i in 1 2 3 4 5;do
for pi in `cat ../paratxt/pi.txt`;do
for dr in `cat ../paratxt/dr.txt`;do
for ef in `cat ../paratxt/ef.txt`;do
qsub -l s_vmem=8G,mem_req=8G super_exe_drug.sh $pi $dr $ef
done
done
done
done
