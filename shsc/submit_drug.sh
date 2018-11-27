#!/bin/bash
#$ -S /bin/bash
#$ -cwd

for pi in `cat ../paratxt/pi.txt`;do
for dr in `cat ../paratxt/dr.txt`;do
for ef in `cat ../paratxt/ef.txt`;do
qsub super_exe_drug.sh $pi $dr $ef
done
done
done
