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
from Tumorcell_compe import Tumor_cell
from Janitor_ver2 import Janitor
from Visualizer_two_ver2 import Visualizer_two
from Plotter import Plotter
import pickle
import os
import re
homedir = os.path.abspath(os.path.dirname(__file__))
homedir = re.sub("/python", "", homedir)

pid = str(os.getpid())

import argparse
parser = argparse.ArgumentParser()
parser.add_argument("--func", "-fu", choices=["dire1", "dire2"], default="dire2")
parser.add_argument("--SIZE", "-si", type=int, default=777)
parser.add_argument("--AVERAGE", "-av", type=float, default=10)
parser.add_argument("--DISPERSION", "-di", type=float, default=2)
parser.add_argument("--MAXNUM", "-ma", type=int, default=110000)
parser.add_argument("--INTERVAL", "-in", default=1, type=int)
parser.add_argument("--AROUND", "-ar", default=15, type=int)
parser.add_argument("--WEIGHT1", "-we1", default=1.02, type=float)
parser.add_argument("--WEIGHT2", "-we2", default=0.98, type=float)
parser.add_argument("--funcM", "-fuM", choices=["mortal1", "mortal2"], default="mortal2")
parser.add_argument("--MTRATE", "-mt", default=0.0000005, type=float)
parser.add_argument("--DRUGTIMES", "-dr", default="10,8")
parser.add_argument("--EFFECT", "-ef", default=0.28, type=float)
parser.add_argument("--PID", "-pi", default=30189)
parser.add_argument("--POISSON", "-po", default=10, type=float)
args = parser.parse_args()

binary_fix = homedir + "/binary/" + str(args.PID)
janitorbinary = binary_fix + "_janitor.binaryfile"
with open(janitorbinary, mode='rb') as f:
    janitor = pickle.load(f)
visualizerbinary = binary_fix + "_visualizer.binaryfile"
with open(visualizerbinary, mode='rb') as f:
    visualizer = pickle.load(f)

Tumor_cell.receive_value(args.AVERAGE, args.DISPERSION, args.AROUND, args.WEIGHT1, args.WEIGHT2, args.MTRATE, args.DRUGTIMES, args.EFFECT)
janitor.receive_value(args.func, args.SIZE, args.MAXNUM)
Tumor_cell.prepare_drug(janitor.t)

while janitor.n < janitor.MAXNUM and janitor.n > 0:

    for cell in janitor.celllist:
        if cell.dead == 0:
            cell.waittime_minus()
            cell.decide_prolife()
        else:
            pass

    Tumor_cell.radial_prolife_up(janitor.field, janitor.on, janitor.func, janitor.celllist, janitor.timedic, janitor.driver_list)

    if Cell.DR_INTERVAL != 0:
        for cell in janitor.celllist:
            cell.count_around(janitor.heatmap)
            cell.drugged_infinity(janitor.t)

    if Cell.DR_INTERVAL == 0:
        for cell in janitor.celllist:
            cell.count_around(janitor.heatmap)
            cell.drugged_infinity_continued()

    Tumor_cell.drtime_adjust(janitor.t)
    janitor.refresh_heatmap()

    for cell in janitor.celllist:
        if args.funcM == "mortal1":
            cell.mortal1_drug(janitor.field)
        if args.funcM == "mortal2":
            cell.mortal2_drug(janitor.field)
        if cell.dead == 0:
            cell.waittime_gamma()
        cell.update_heatmap(janitor.heatmap)

    janitor.append_cell_num()
    visualizer.plot_append_heatmap_graph(janitor.heatmap, janitor.t, janitor.tlist, janitor.onelist, janitor.twolist, plot=False, append=False)
    janitor.count_cell_num()
    janitor.t += 1

if args.funcM == "mortal1":
    para = pid + "_" + str(args.PID) + "m1_" + "ad" + str(args.AVERAGE) + "_" + str(args.DISPERSION) + "r" + str(args.AROUND) + "mt" + str(args.MTRATE) + "d" + str(args.DRUGTIMES) + "e" + str(args.EFFECT)
if args.funcM == "mortal2":
    para = pid + "_" + str(args.PID) + "m2_" + "ad" + str(args.AVERAGE) + "_" + str(args.DISPERSION) + "r" + str(args.AROUND) + "mt" + str(args.MTRATE) + "w" + str(args.WEIGHT1) + "_" + str(args.WEIGHT2) + "d" + str(args.DRUGTIMES) + "e" + str(args.EFFECT)

janitor.list_adjust()
janitor.make_idlist()

binary_fix = homedir + "/binary/" + pid
janitorbinary = binary_fix + "_debugjanitor.binaryfile"
with open(janitorbinary, mode='wb') as f:
    pickle.dump(janitor, f)

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
