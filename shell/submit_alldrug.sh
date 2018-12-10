#!/bin/bash
#$ -S /bin/bash
#$ -cwd

cdir=$(cd $(dirname $0) && pwd)
hdir=${cdir%/*}
rdir=$hdir/result/
for i in 1 2 3 4 5 6 7 8 9 10;do
for mt in `cat ../paratxt/mt.txt`;do
for dr in `cat ../paratxt/dr.txt`;do
for ef in `cat ../paratxt/ef.txt`;do
for we1 in `cat ../paratxt/we1.txt`;do
for we2 in `cat ../paratxt/we2.txt`;do
fname=$rdir
fname+=$i
fname+=$mt
fname+=$dr
fname+=$ef
fname+=$we1
fname+=$we2
fname=${fname//./_}
touch $fname
qsub -l -e $fname -o $fname s_vmem=12G,mem_req=12G super_exe_alldrug.sh $mt $dr $ef $we1 $we2 $fname
done
done
done
done
done
done
