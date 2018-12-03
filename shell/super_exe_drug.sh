#!/bin/bash
#$ -S /bin/bash
#$ -cwd


python ../python/tumor_exe_drug.py >&1 >&2 -pi $1 -dr $2 -ef $3
