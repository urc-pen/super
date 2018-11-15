#!/bin/bash
#$ -S /bin/bash
#$ -cwd

python ../pysc/tumor_exe_predrug.py >&1 >&2 -av $1 -ar $2 -we1 $3 -we2 $4 -fuM $5 -mt $6
