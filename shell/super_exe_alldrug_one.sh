#!/bin/bash
#$ -S /bin/bash
#$ -cwd

for i in 1 2 3 4 5 6 7 8 9 10;do
python ../python/tumor_exe_alldrug.py >&1 >&2
done
