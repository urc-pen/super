#!/bin/bash
#$ -S /bin/bash
#$ -cwd


python ../pysc tumor_exe_plotmutation.py -av $av -en $en -fu2 $fu2 -mt $mt -po $po -tu $tu
