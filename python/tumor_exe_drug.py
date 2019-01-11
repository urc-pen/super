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
parser.add_argument("--DRUGTIMES", "-dr", default="10,0")
parser.add_argument("--EFFECT", "-ef", default=0.28, type=float)
parser.add_argument("--PID", "-pi", default=30189)
parser.add_argument("--POISSON", "-po", default=10, type=float)
args = parser.parse_args()

binary_fix = homedir + "/binary/" + args.PID
janitorbinary = binary_fix + "_janitor.binaryfile"
with open(janitorbinary, mode='rb') as f:
    janitor = pickle.load(f)
visualizerbinary = binary_fix + "_visualizer.binaryfile"
with open(visualizerbinary, mode='rb') as f:
    visualizer = pickle.load(f)

Tumor_cell.receive_value(args.AVERAGE, args.DISPERSION, args.AROUND, args.WEIGHT1, args.WEIGHT2, args.MTRATE, args.DRUGTIMES, args.EFFECT)
janitor.receive_value(args.func, args.SIZE, args.MAXNUM)
Tumor_cell.prepare_drug(janitor.t)

TIME = janitor.t
redflag = 0
cellnumlist = []
cell1numlist = []
cell2numlist = []

cellnumlist.append(janitor.n)
cell1numlist.append(janitor.cell_one_num)
cell2numlist.append(janitor.cell_two_num)

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
    visualizer.plot_append_heatmap_graph(janitor.heatmap, janitor.t, janitor.tlist, janitor.onelist, janitor.twolist, plot=False, append=True)
    janitor.count_cell_num()
    janitor.count_type()
    if janitor.cell_two_num >= 10000 and redflag == 0:
        REDTIME = janitor.t
        redflag = 1
    janitor.t += 1
    cellnumlist.append(janitor.n)
    cell1numlist.append(janitor.cell_one_num)
    cell2numlist.append(janitor.cell_two_num)

ENDTIME = janitor.t

if args.funcM == "mortal1":
    para = pid + "_" + args.PID + "m1_" + "ad" + str(args.AVERAGE) + "_" + str(args.DISPERSION) + "r" + str(args.AROUND) + "mt" + str(args.MTRATE) + "d" + str(args.DRUGTIMES) + "e" + str(args.EFFECT)
if args.funcM == "mortal2":
    para = pid + "_" + args.PID + "m2_" + "ad" + str(args.AVERAGE) + "_" + str(args.DISPERSION) + "r" + str(args.AROUND) + "mt" + str(args.MTRATE) + "w" + str(args.WEIGHT1) + "_" + str(args.WEIGHT2) + "d" + str(args.DRUGTIMES) + "e" + str(args.EFFECT)

timepre = homedir + "/result/txtstore/" + para + ".txt"
RESULT = ENDTIME - TIME
RESULT2 = REDTIME - TIME
TXTTIME = str(janitor.n) + "_" + str(TIME) + "_" + str(ENDTIME) + "_" + str(REDTIME) + "_" + str(RESULT) + "_" + str(RESULT2)

maped_cellnumlist = map(str, cellnumlist)
str_cellnumlist = ",".join(maped_cellnumlist)

maped_cell1numlist = map(str, cell1numlist)
str_cell1numlist = ",".join(maped_cell1numlist)

maped_cell2numlist = map(str, cell2numlist)
str_cell2numlist = ",".join(maped_cell2numlist)

str_numlist = str_cellnumlist + "//" + str_cell1numlist + "//" + str_cell2numlist
with open(timepre, mode='w') as f:
    f.write(str_numlist)

visualizer.save_heatmap_graph("anime", para, janitor.heatmap, janitor.tlist, janitor.onelist, janitor.twolist)
