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
parser.add_argument("--MAXNUM", "-ma", type=int, default=110000)
parser.add_argument("--INTERVAL", "-in", default=1, type=int)
parser.add_argument("--AROUND", "-ar", default=10, type=int)
parser.add_argument("--WEIGHT1", "-we1", default=0.9, type=float)
parser.add_argument("--WEIGHT2", "-we2", default=1.1, type=float)
parser.add_argument("--funcM", "-fuM", choices=["mortal1", "mortal2"], default="mortal2")
parser.add_argument("--MTRATE", "-mt", default=0.00001, type=float)
parser.add_argument("--DRUGTIMES", "-dr", default="10,13")
parser.add_argument("--EFFECT", "-ef", default=0.2, type=float)
parser.add_argument("--PID", "-pi")
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
print("薬剤耐性変異の入る確率:{}".format(args.MTRATE))
print("薬剤投与スケジュール:{}".format(args.DRUGTIMES))
print("薬剤の強さ:{}".format(args.EFFECT))
if args.funcM == "mortal2":
    print("type1の競争係数（<1）:{}".format(args.WEIGHT1))
    print("type2の競争係数（>1）:{}".format(args.WEIGHT2))

binary_fix = homedir + "/binary/" + str(args.PID)
listbinary = binary_fix + "_list.binaryfile"
with open(listbinary, mode='rb') as f:
    list = pickle.load(f)
fieldbinary = binary_fix + "_field.binaryfile"
with open(fieldbinary, mode='rb') as f:
    field = pickle.load(f)
heatmapbinary = binary_fix + "_heatmap.binaryfile"
with open(heatmapbinary, mode='rb') as f:
    heatmap = pickle.load(f)
timedicbinary = binary_fix + "_timedic.binaryfile"
with open(timedicbinary, mode='rb') as f:
    timedic = pickle.load(f)
mtlistbinary = binary_fix + "_mtlist.binaryfile"
with open(mtlistbinary, mode='rb') as f:
    mtlist = pickle.load(f)

Tumor_cell.receive_value(args.AVERAGE, args.DISPERSION, args.AROUND, args.WEIGHT1, args.WEIGHT2, args.MTRATE, args.DRUGTIMES, args.EFFECT)
Tumor_janitor.receive_value(args.func, args.SIZE, args.MAXNUM, args.INTERVAL)
Tumor_janitor.create_value("drug")
Tumor_janitor.receive_field_heatmap(field, heatmap)
Tumor_cell.receive_list(list, timedic, mtlist)
Tumor_janitor.append_cell_num()
Tumor_janitor.first_heatmap_graph()

while Janitor.n < Janitor.MAXNUM and Janitor.cell_two_num < 50000 and Janitor.t < 2000:

    for cell in Cell.celllist:
        if cell.dead == 0:
            cell.waittime_minus()
            cell.decide_prolife()
        else:
            pass

    Tumor_cell.radial_prolife(Janitor.field, Janitor.on, Janitor.func)

    for cell in Cell.celllist:
        cell.count_around(Janitor.heatmap)
        cell.drugged_infinity(Janitor.t)

    Tumor_cell.drtime_adjust(Janitor.t)
    Janitor.refresh_heatmap()

    for cell in Cell.celllist:
        if args.funcM == "mortal1":
            cell.mortal1_drug(Janitor.field)
        if args.funcM == "mortal2":
            cell.mortal2_drug(Janitor.field)
        if cell.dead == 0:
            cell.waittime_gamma()
        cell.update_heatmap(Janitor.heatmap)

    Tumor_janitor.append_cell_num()
    Tumor_janitor.plot_append_heatmap_graph(plot=False, append=True)
    Tumor_janitor.count_type()
    Janitor.count_cell_num()
    Janitor.t += 1

    if Janitor.n >= Janitor.MAXNUM:
        break

if args.funcM == "mortal1":
    para = pid + "_" + args.PID + "m1_" + "ad" + str(args.AVERAGE) + "_" + str(args.DISPERSION) + "r" + str(args.AROUND) + "mt" + str(args.MTRATE) + "d" + str(args.DRUGTIMES) + "e" + str(args.EFFECT)
if args.funcM == "mortal2":
    para = pid + "_" + args.PID + "m2_" + "ad" + str(args.AVERAGE) + "_" + str(args.DISPERSION) + "r" + str(args.AROUND) + "mt" + str(args.MTRATE) + "w" + str(args.WEIGHT1) + "_" + str(args.WEIGHT2) + "d" + str(args.DRUGTIMES) + "e" + str(args.EFFECT)

Tumor_janitor.save_heatmap_graph("anime", para)
Tumor_cell.list_adjust()
Tumor_cell.make_idlist_includedead(Janitor.field)
Plotter.receive_value(args.POISSON)
Plotter.plot_mutation(Tumor_cell.idlist, Tumor_cell.driver_list)
newicktxt = homedir + "/newick.txt"
Plotter.write_newick(Tumor_cell.idlist, Cell.celllist, Tumor_cell.timedic, newicktxt)
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
