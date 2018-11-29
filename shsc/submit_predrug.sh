#!/bin/bash
#$ -S /bin/bash
#$ -cwd

for i in 1 2 3 4 5 6 7 8 9 10;do
for we1 in `cat ../paratxt/we1.txt`;do
for we2 in `cat ../paratxt/we2.txt`;do
qsub super_exe_predrug.sh $we1 $we2
done
done
done
