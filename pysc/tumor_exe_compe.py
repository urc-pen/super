import numpy as np
import random
import math
import fractions
import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
import pyper as pr
from Cell import Cell
from Janitor import Janitor
from Tumorcell_compe import Tumor_cell_compe
from Tumorjanitor import Tumor_janitor
from Plotter import Plotter
import os
import re
homedir = os.path.abspath(os.path.dirname(__file__))
homedir = re.sub("/pysc", "", homedir)

pid = str(os.getpid())

import argparse
parser = argparse.ArgumentParser()
parser.add_argument("--func", "-fu", choices=["dire1", "dire2"], default="dire2")
parser.add_argument("--SIZE", "-si", type=int, default=201)
parser.add_argument("--AVERAGE", "-av", type=float, default=15)
parser.add_argument("--DISPERSION", "-di", type=float, default=2)
parser.add_argument("--MAXNUM", "-ma", type=int, default=6000)
parser.add_argument("--ENV", "-en", default=4000)
parser.add_argument("--INTERVAL", "-in", default=1, type=int)
parser.add_argument("--POISSON", "-po", default=10)
parser.add_argument("--AROUND", "-ar", default=10, type=int)
parser.add_argument("--WEIGHT", "-we", default=0.2, type=float)
parser.add_argument("--funcM", "-fuM", choices=["mortal1", "mortal2"], default="mortal1")
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
if args.funcM == "mortal2":
    print("同種の競争係数（<1）:{}".format(args.WEIGHT))

Tumor_cell_compe.receive_value(args.AVERAGE, args.DISPERSION, args.ENV, args.AROUND, args.WEIGHT)
Tumor_janitor.receive_value(args.func, args.SIZE, args.MAXNUM, args.INTERVAL)
Janitor.set_field()
Janitor.set_heatmap()
Tumor_cell_compe.set_first_cell(Janitor.field, Janitor.on)
Tumor_janitor.first_heatmap_graph()

while Janitor.n < Janitor.MAXNUM:

    for cell in Cell.celllist:
        if cell.dead == 0:
            cell.waittime_minus()
            cell.decide_prolife()
        else:
            pass

    Tumor_cell_compe.radial_prolife(Janitor.field, Janitor.on, Janitor.func)

    for cell in Cell.celllist:
        cell.count_around(Janitor.heatmap)

    Janitor.refresh_heatmap()

    for cell in Cell.celllist:
        if args.funcM == "mortal1":
            cell.mortal1(Janitor.field)
        if args.funcM == "mortal2":
            cell.mortal2(Janitor.field)
        cell.update_heatmap(Janitor.heatmap)

    Tumor_janitor.append_cell_num()
    Tumor_janitor.plot_heatmap_graph()
    Janitor.count_cell_num()
    Janitor.t += 1

    if Janitor.n >= Janitor.MAXNUM:
        break

Tumor_janitor.count()
