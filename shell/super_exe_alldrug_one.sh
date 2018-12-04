#!/bin/bash
#$ -S /bin/bash
#$ -cwd


python ../python/tumor_exe_alldrug.py >&1 >&2
