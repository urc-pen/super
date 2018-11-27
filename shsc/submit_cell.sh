#!/bin/bash
#$ -S /bin/bash
#$ -cwd

for av in `cat ../paratxt/av2.txt`;do
for di in `cat ../paratxt/di.txt`;do
qsub super_exe_cell.sh $av $di
done
done
