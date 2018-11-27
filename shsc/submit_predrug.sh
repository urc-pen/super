#!/bin/bash
#$ -S /bin/bash
#$ -cwd

for i in 1 2 3 4 5;do
qsub super_exe_predrug.sh
done
