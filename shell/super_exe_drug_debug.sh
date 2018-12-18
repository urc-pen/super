#!/bin/bash
#$ -S /bin/bash
#$ -cwd


python ../python/tumor_exe_drug_debug.py >&1 >&2
