#!/bin/bash
#$ -S /bin/bash
#$ -cwd

python ../pysc/tumor_exe.py -av $1 -en $2 -fu2 $3 -mt $4 -po $5 -tu $6 >&1 >&2　
