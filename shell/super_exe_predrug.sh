#!/bin/bash
#$ -S /bin/bash
#$ -cwd

python ../python/tumor_exe_predrug.py >&1 >&2
