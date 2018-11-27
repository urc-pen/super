#!/bin/bash
#$ -S /bin/bash
#$ -cwd

python ../pysc/tumor_exe_drug.py >&1 >&2 -av $1 -di $2
