#!/bin/bash
#$ -S /bin/bash
#$ -cwd

for i in 1 2 3 4 5 6 7 8 9 10;do
for i in 1 2 3 4 5 6 7 8 9 10;do
qsub super_exe_predrug.sh
done
done
