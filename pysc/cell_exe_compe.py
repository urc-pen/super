import numpy as np
import random
import math
import fractions
import matplotlib

import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
import pyper as pr
from Cell import Cell
from Janitor import Janitor
from Cell_compe import Cell_compe
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
parser.add_argument("--AVERAGE", "-av", type=float, default=10)
parser.add_argument("--DISPERSION", "-di", type=float, default=2)
parser.add_argument("--MAXNUM", "-ma", type=int, default=100000)
parser.add_argument("--INTERVAL", "-in", default=1, type=int)
parser.add_argument("--AROUND", "-ar", default=15, type=int)
parser.add_argument("--WEIGHT", "-we", default=1.1, type=float)
parser.add_argument("--funcM", "-fuM", choices=["mortal1", "mortal2"], default="mortal1")
parser.add_argument("--POISSON", "-po", default=10, type=float)
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
    print("競争係数:{}".format(args.WEIGHT))

Cell_compe.receive_value(args.AVERAGE, args.DISPERSION, args.AROUND, args.WEIGHT)
Janitor.receive_value(args.func, args.SIZE, args.MAXNUM, args.INTERVAL)
Janitor.set_field()
Janitor.set_heatmap()
Cell_compe.set_first_cell(Janitor.field, Janitor.on)
Janitor.append_cell_num()
Janitor.first_heatmap_graph()

while Janitor.n < Janitor.MAXNUM:

    for cell in Cell.celllist:
        if cell.dead == 0:
            cell.waittime_minus()
            cell.decide_prolife()
        else:
            pass

    Cell_compe.radial_prolife(Janitor.field, Janitor.on, Janitor.func)

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

    Janitor.append_cell_num()
    Janitor.plot_append_heatmap_graph(plot=False, append=True)
    Janitor.count_cell_num()
    Janitor.t += 1

    if Janitor.n >= Janitor.MAXNUM:
        break

if args.funcM == "mortal1":
    para = pid + "m1_" + "ad" + str(args.AVERAGE) + "_" + str(args.DISPERSION) + "r" + str(args.AROUND)
if args.funcM == "mortal2":
    para = pid + "m2_" + "ad" + str(args.AVERAGE) + "_" + str(args.DISPERSION) + "r" + str(args.AROUND) + "w" + str(args.WEIGHT)
Janitor.save_heatmap_graph("anime", para)
Cell_compe.list_adjust()
Cell_compe.make_idlist(Janitor.field)
Plotter.receive_value(args.POISSON)
Plotter.plot_mutation(Cell_compe.idlist, Cell_compe.driver_list)
newicktxt = homedir + "/newick.txt"
Plotter.write_newick(Cell_compe.idlist, Cell.celllist, Cell_compe.timedic, newicktxt)
pidcsv = homedir + pid + ".csv"
Plotter.df.to_csv(pidcsv)
rfile = homedir + "/Rsc/illust.R"
r2file = homedir + "/Rsc/tree.R"
r = pr.R(use_pandas='True')
r2 = pr.R()
hpre = homedir + "/result/pdfstore/" + para
tpre = homedir + "/result/txtstore/" + para
treepre = homedir + "/result/treestore/" + para
r.assign("pidcsv", pidcsv)
r.assign("hpre", hpre)
r.assign("tpre", tpre)
r("source(file='{}')".format(str(rfile)))
r2.assign("newicktxt", newicktxt)
r2.assign("treepre", treepre)
r2("source(file='{}')".format(str(r2file)))
os.remove(pidcsv)
os.remove(newicktxt)
