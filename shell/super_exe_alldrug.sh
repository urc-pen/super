#!/bin/bash
#$ -S /bin/bash
#$ -cwd


python ../python/tumor_exe_alldrug.py >&1 >&2 -mt $1 -dr $2 -ef $3 -we1 $4 -we2 $5 -fn $6
