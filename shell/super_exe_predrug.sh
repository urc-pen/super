#!/bin/bash
#$ -S /bin/bash
#$ -cwd

python ../python/tumor_exe_predrug.py >&1 >&2 -we1 $1 -we2 $2
