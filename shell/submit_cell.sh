#!/bin/bash
#$ -S /bin/bash
#$ -cwd

for av in `cat ../paratxt/av2.txt`;do
for di in `cat ../paratxt/di.txt`;do
qsub -l s_vmem=8G,mem_req=8G super_exe_cell.sh $av $di
done
done
