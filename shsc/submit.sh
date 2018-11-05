#!/bin/bash
#$ -S /bin/bash
#$ -cwd

for av in ｀cat ../paratxt/av.txt｀
  for en in ｀cat ../paratxt/en.txt｀
    for fu2 in ｀cat ../paratxt/fu2.txt｀
      for mt in ｀cat ../paratxt/mt.txt｀
        for po in ｀cat ../paratxt/po.txt｀
          for tu in ｀cat ../paratxt/tu.txt｀
          do
            qsub super_exe.sh $av $en $fu2 $mt $po $tu
          done
