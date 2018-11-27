import numpy as np
import random
import math
import fractions
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
import pyper as pr
from Cell import Cell
from Janitor import Janitor
from Tumorcell_compe import Tumor_cell
from Tumor_janitor import Tumor_janitor
from Plotter import Plotter
import pickle
import os
import re
homedir = os.path.abspath(os.path.dirname(__file__))
homedir = re.sub("/pysc", "", homedir)

pid = str(os.getpid())

import argparse
parser = argparse.ArgumentParser()
parser.add_argument("--func", "-fu", choices=["dire1", "dire2"], default="dire2")
parser.add_argument("--SIZE", "-si", type=int, default=777)
parser.add_argument("--AVERAGE", "-av", type=float, default=15)
parser.add_argument("--DISPERSION", "-di", type=float, default=2)
parser.add_argument("--MAXNUM", "-ma", type=int, default=100000)
parser.add_argument("--INTERVAL", "-in", default=1, type=int)
parser.add_argument("--AROUND", "-ar", default=15, type=int)
parser.add_argument("--WEIGHT1", "-we1", default=0.9, type=float)
parser.add_argument("--WEIGHT2", "-we2", default=1.1, type=float)
parser.add_argument("--funcM", "-fuM", choices=["mortal1", "mortal2"], default="mortal2")
parser.add_argument("--MTRATE", "-mt", default=0.00005, type=float)
parser.add_argument("--DRUGTIMES", "-dr", default="80,85,100,105")
parser.add_argument("--EFFECT", "-ef", default=0.5, type=float)
args = parser.parse_args()

if args.SIZE % 2 != 1:
    raise InvaridNumber("奇数を入力してください")

print("分裂方法:{}".format(args.func))
print("フィールドの大きさ:{}".format(args.SIZE))
print("最大許容細胞数:{}".format(args.MAXNUM))
print("おおよその細胞周期:{}".format(args.AVERAGE))
print("細胞周期のばらつき:{}".format(args.DISPERSION))
print("描画のインターバル:{}".format(args.INTERVAL))
print("競争モデル:{}".format(args.funcM))
print("ローカルの計測範囲:{}".format(args.AROUND))
print("薬剤耐性変異の入る確率:{}".format(args.MTRATE))
if args.funcM == "mortal2":
    print("type1の競争係数（<1）:{}".format(args.WEIGHT1))
    print("type2の競争係数（>1）:{}".format(args.WEIGHT2))

Tumor_cell.receive_value(args.AVERAGE, args.DISPERSION, args.AROUND, args.WEIGHT1, args.WEIGHT2, args.MTRATE, args.DRUGTIMES, args.EFFECT)
Tumor_janitor.receive_value(args.func, args.SIZE, args.MAXNUM, args.INTERVAL)
Tumor_janitor.create_value("drug")
Janitor.set_field()
Janitor.set_heatmap()
Tumor_cell.set_first_cell(Janitor.field, Janitor.on)
Tumor_janitor.append_cell_num()
Tumor_janitor.first_heatmap_graph()

while Janitor.n < Janitor.MAXNUM:

    for cell in Cell.celllist:
        if cell.dead == 0:
            cell.waittime_minus()
            cell.decide_prolife()
        else:
            pass

    Tumor_cell.radial_prolife(Janitor.field, Janitor.on, Janitor.func)

    for cell in Cell.celllist:
        cell.count_around(Janitor.heatmap)

    Janitor.refresh_heatmap()

    for cell in Cell.celllist:
        if args.funcM == "mortal1":
            cell.mortal1(Janitor.field)
        if args.funcM == "mortal2":
            cell.mortal2(Janitor.field)
        if cell.dead == 0:
            cell.waittime_gamma()
        cell.update_heatmap(Janitor.heatmap)

    Tumor_janitor.append_cell_num()
    Tumor_janitor.plot_append_heatmap_graph(plot=False, append=False)
    Janitor.count_cell_num()
    Janitor.t += 1

    if Janitor.n >= Janitor.MAXNUM:
        break

if args.funcM == "mortal1":
    para = pid + "m1_" + "ad" + str(args.AVERAGE) + "_" + str(args.DISPERSION) + "r" + str(args.AROUND) + "mt" + str(args.MTRATE)
if args.funcM == "mortal2":
    para = pid + "m2_" + "ad" + str(args.AVERAGE) + "_" + str(args.DISPERSION) + "r" + str(args.AROUND) + "mt" + str(args.MTRATE) + "w" + str(args.WEIGHT1) + "_" + str(args.WEIGHT2)
Tumor_janitor.save_heatmap_graph("pic", para)

binary_fix = homedir + "/binary/" + pid
listbinary = binary_fix + "_list.binaryfile"
with open(listbinary, mode='wb') as f:
    pickle.dump(Cell.celllist, f)
fieldbinary = binary_fix + "_field.binaryfile"
with open(fieldbinary, mode='wb') as f:
    pickle.dump(Janitor.field, f)
heatmapbinary = binary_fix + "_heatmap.binaryfile"
with open(heatmapbinary, mode='wb') as f:
    pickle.dump(Janitor.heatmap, f)
timedicbinary = binary_fix + "_timedic.binaryfile"
with open(timedicbinary, mode='wb') as f:
    pickle.dump(Tumor_cell.timedic, f)
mtlistbinary = binary_fix + "_mtlist.binaryfile"
with open(mtlistbinary, mode='wb') as f:
    pickle.dump(Tumor_cell.driver_list, f)
