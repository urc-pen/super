#!/bin/bash
#$ -S /bin/bash
#$ -cwd

for av in `cat ../paratxt/av2.txt`;do
for ar in `cat ../paratxt/ar.txt`;do
for we in `cat ../paratxt/we.txt`;do
for fuM in `cat ../paratxt/fuM.txt`;do
for mt in `cat ../paratxt/mt2.txt`;do
qsub super_exe.sh $av $ar $we $fuM $mt
done
done
done
done
done
