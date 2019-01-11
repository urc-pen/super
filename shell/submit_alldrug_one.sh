#!/bin/bash
#$ -S /bin/bash
#$ -cwd

for i in 1 2 3 4 5 6 7 8 9 10;do
qsub -l s_vmem=18G,mem_req=18G super_exe_alldrug_one.sh
done
