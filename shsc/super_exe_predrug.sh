#!/bin/bash
#$ -S /bin/bash
#$ -cwd

python ../pysc/tumor_exe_predrug.py >&1 >&2 
