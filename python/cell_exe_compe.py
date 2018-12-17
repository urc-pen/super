import numpy as np
import random
import math
import fractions
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
import pyper as pr
from Janitor import Janitor
from Cell_compe import Cell_compe
from Plotter import Plotter
from Visualizer import Visualizer
import pickle
import os
import re
homedir = os.path.abspath(os.path.dirname(__file__))
homedir = re.sub("/python", "", homedir)

pid = str(os.getpid())

import argparse
parser = argparse.ArgumentParser()
parser.add_argument("--func", "-fu", choices=["dire1", "dire2"], default="dire1")
parser.add_argument("--SIZE", "-si", type=int, default=777)
parser.add_argument("--AVERAGE", "-av", type=float, default=10)
parser.add_argument("--DISPERSION", "-di", type=float, default=1000)
parser.add_argument("--MAXNUM", "-ma", type=int, default=100000)
parser.add_argument("--INTERVAL", "-in", default=1, type=int)
parser.add_argument("--AROUND", "-ar", default=15, type=int)
parser.add_argument("--WEIGHT", "-we2", default=1.1, type=float)
parser.add_argument("--funcM", "-fuM", choices=["mortal1", "mortal2"], default="mortal1")
parser.add_argument("--POISSON", "-po", default=10, type=float)
args = parser.parse_args()

janitor = Janitor()
visualizer = Visualizer()
Cell_compe.receive_value(args.AVERAGE, args.DISPERSION, args.AROUND, args.WEIGHT)
janitor.receive_value(args.func, args.SIZE, args.MAXNUM)
visualizer.receive_value(args.INTERVAL)
janitor.set_field()
janitor.set_heatmap()
Cell_compe.set_first_cell(janitor.field, janitor.on, janitor.celllist)
visualizer.append_cell_num(janitor.heatmap, janitor.t)
visualizer.first_heatmap_graph(janitor.heatmap)

while janitor.n < janitor.MAXNUM:

    for cell in janitor.celllist:
        if cell.dead == 0:
            cell.waittime_minus()
            cell.decide_prolife()
        else:
            pass

    Cell_compe.radial_prolife_up(janitor.field, janitor.on, janitor.func, janitor.celllist, janitor.timedic)

    for cell in janitor.celllist:
        cell.count_around(janitor.heatmap)

    janitor.refresh_heatmap()

    for cell in janitor.celllist:
        if args.funcM == "mortal1":
            cell.mortal1(janitor.field)
        if args.funcM == "mortal2":
            cell.mortal2(janitor.field)
        if cell.dead == 0:
            cell.waittime_gamma()
        cell.update_heatmap(janitor.heatmap)

    visualizer.append_cell_num(janitor.heatmap, janitor.t)
    visualizer.plot_append_heatmap_graph(janitor.heatmap, janitor.t, plot=False, append=True)
    janitor.count_cell_num()
    janitor.t += 1

    if janitor.n >= janitor.MAXNUM:
        break

if args.funcM == "mortal1":
    para = pid + "m1_" + "ad" + str(args.AVERAGE) + "_" + str(args.DISPERSION) + "r" + str(args.AROUND)
if args.funcM == "mortal2":
    para = pid + "m2_" + "ad" + str(args.AVERAGE) + "_" + str(args.DISPERSION) + "r" + str(args.AROUND) + "w" + str(args.WEIGHT)
visualizer.save_heatmap_graph("anime", para, janitor.heatmap)
janitor.list_adjust()
janitor.make_idlist()
Plotter.receive_value(args.POISSON)
Plotter.plot_mutation(janitor.idlist, janitor.driver_list)
newicktxt = homedir + "/newick" + pid + ".txt"
Plotter.write_newick(janitor.idlist, janitor.celllist, janitor.timedic, newicktxt)
pidcsv = homedir + "/" + pid + ".csv"
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
binary_fix = homedir + "/binary/" + pid
janitorbinary = binary_fix + "_janitor.binaryfile"
with open(janitorbinary, mode='wb') as f:
    pickle.dump(janitor, f)
