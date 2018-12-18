#!/bin/bash
#$ -S /bin/bash
#$ -cwd

qsub -l s_vmem=13G,mem_req=13G super_exe_drug_debug.sh
