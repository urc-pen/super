#!/bin/bash
#$ -S /bin/bash
#$ -cwd
python ../pysc/cell_exe_compe.py -av $1 -di $2 >&1 >&2
