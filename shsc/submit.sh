#!/bin/bash
#$ -S /bin/bash
#$ -cwd

for av in ｀cat ../paratxt/av.txt｀;do
for en in ｀cat ../paratxt/en.txt｀;do
for fu2 in ｀cat ../paratxt/fu2.txt｀;do
for mt in ｀cat ../paratxt/mt.txt｀;do
for po in ｀cat ../paratxt/po.txt｀;do
for tu in ｀cat ../paratxt/tu.txt｀;do
qsub super_exe.sh $av $en $fu2 $mt $po $tu
done
done
done
done
done
done
