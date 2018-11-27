#!/bin/bash
#$ -S /bin/bash
#$ -cwd


python ../pysc/cell_exe_compe.py >&1 >&2 -av $1 -di $2
