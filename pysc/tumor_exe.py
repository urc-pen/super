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
from Tumorcell import Tumor_cell
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
parser.add_argument("--SIZE", "-si", type=int, default=721)
parser.add_argument("--AVERAGE", "-av", type=float, default=15)
parser.add_argument("--DISPERSION", "-di", type=float, default=2)
parser.add_argument("--MAXNUM", "-ma", type=int, default=100000)
parser.add_argument("--ENV", "-en", default=4000, type=int)
parser.add_argument("--MTRATE", "-mt", default=0.001, type=float)
parser.add_argument("--INTERVAL", "-in", default=100, type=int)
parser.add_argument("--POISSON", "-po", default=10, type=float)
parser.add_argument("--TUMORSPEED", "-tu", default=3, type=float)
parser.add_argument("--func2", "-fu2", choices=["cycle", "mortal"], default="mortal")
parser.add_argument("--AROUND", "-ar", default=10, type=int)
args = parser.parse_args()

if args.SIZE % 2 != 1:
    raise InvaridNumber("奇数を入力してください")

print("分裂方法:{}".format(args.func))
print("フィールドの大きさ:{}".format(args.SIZE))
print("最大許容細胞数:{}".format(args.MAXNUM))
print("おおよその細胞周期:{}".format(args.AVERAGE))
print("細胞周期のばらつき:{}".format(args.DISPERSION))
print("ドライバー変異の起きる確率:{}".format(args.MTRATE))
print("描画のインターバル:{}".format(args.INTERVAL))
print("ポアソン分布の期待値:{}".format(args.POISSON))
if args.func2 == "cycle":
    print("ガン細胞の細胞周期の短くなる割合:{}".format(args.TUMORSPEED))
if args.func2 == "mortal":
    print("環境収容力:{}".format(args.ENV))

Tumor_cell.receive_value(args.AVERAGE, args.DISPERSION, args.ENV, args.MTRATE, args.TUMORSPEED)
Tumor_janitor.receive_value(args.func, args.SIZE, args.MAXNUM, args.INTERVAL)
Janitor.set_field()
Janitor.set_heatmap()
Tumor_cell.set_first_cell(Janitor.field, Janitor.on)
Tumor_janitor.first_heatmap_graph()

while Janitor.n < Janitor.MAXNUM:

    for cell in Cell.celllist:
        if cell.dead == 0:
            cell.waittime_minus()
            cell.decide_prolife()
        else:
            pass

    Tumor_cell.radial_prolife(Janitor.field, Janitor.on, Janitor.func)

    Tumor_cell.countall(Janitor.heatmap)
    Janitor.refresh_heatmap()

    for cell in Cell.celllist:
        if args.func2 == "cycle":
            cell.adjust_waittime()
        if args.func2 == "mortal":
            cell.tumor_dead_or_alive(Janitor.field)
        cell.update_heatmap(Janitor.heatmap)

    Tumor_janitor.append_cell_num()
    Janitor.count_cell_num()
    Janitor.t += 1

    if Janitor.n >= Janitor.MAXNUM:
        break

strmt = str(args.MTRATE)
dstmt = strmt.replace('.', '_')
if args.func2 == "cycle":
    para = "c" + str(args.TUMORSPEED) + "a_d" + str(args.AVERAGE) + "p" + str(args.POISSON) + "m" + dstmt
if args.func2 == "mortal":
    para = "m" + str(args.ENV) + "a_d" + str(args.AVERAGE) + "p" + str(args.POISSON) + "m" + dstmt

Tumor_janitor.save_heatmap_graph(para)
Tumor_janitor.count()
Tumor_cell.list_adjust()
Tumor_cell.make_idlist(Janitor.field)
Plotter.receive_value(args.POISSON)
Plotter.plot_mutation(Tumor_cell.idlist, Tumor_cell.driver_list, Plotter.POISSON)
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
