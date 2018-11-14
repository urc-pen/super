#!/bin/bash
#$ -S /bin/bash
#$ -cwd


python ../pysc/tumor_exe_predrug.py >&1 >&2 -av $1 -ar $2 -we $3 -fuM $4 -mt $5
