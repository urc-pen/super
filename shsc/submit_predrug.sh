#!/bin/bash
#$ -S /bin/bash
#$ -cwd

for av in `cat ../paratxt/av2.txt`;do
for ar in `cat ../paratxt/ar.txt`;do
for we1 in `cat ../paratxt/we1.txt`;do
for we2 in `cat ../paratxt/we2.txt`;do
for fuM in `cat ../paratxt/fuM.txt`;do
for mt in `cat ../paratxt/mt2.txt`;do
qsub super_exe_predrug.sh $av $ar $we1 $we2 $fuM $mt
done
done
done
done
done
done
