import numpy as np
import random
import math
import fractions
import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap

class Janitor:

    @classmethod
    def receive_value(cls, func, SIZE, MAXNUM):
        Janitor.func = func
        Janitor.SIZE = SIZE                    #フィールドの大きさ
        Janitor.on = int((Janitor.SIZE - 1) / 2)
        Janitor.t = 0
        Janitor.n = 0
        Janitor.MAXNUM = MAXNUM
        Janitor.threelist = [0]
        Janitor.fourlist = [0]
        Janitor.fivelist = [0]
        Janitor.sixlist = [0]
        Janitor.tlist = [0]

    @classmethod
    def set_field(cls):
        Janitor.field = np.full((Janitor.SIZE, Janitor.SIZE), -1, dtype=int)

    @classmethod
    def set_heatmap(cls):
        Janitor.heatmap = np.zeros((Janitor.SIZE, Janitor.SIZE))

    @classmethod
    def first_heatmap_graph(cls):
        fig = plt.figure(figsize=(10, 5))
        Janitor.colors = [(1, 1, 1), (0, 0.2, 0.8), (0, 0.3, 0.7) ,(0.5, 0, 0.5), (1, 0, 0), (0.2, 0.8, 1), (0.5, 0.8, 0.2)]
        cmap_name = 'my_list'
        Janitor.cm = LinearSegmentedColormap.from_list(cmap_name, Janitor.colors, N=7)
        defheatmap = Janitor.heatmap
        for n in range(0, 7):
            defheatmap[0, n] = n
        Janitor.ax1 = fig.add_subplot(1, 2, 1)
        Janitor.ax2 = fig.add_subplot(1, 2, 2)
        Janitor.ax1.plot(Janitor.tlist, Janitor.threelist, label="3", color=Janitor.colors[3])
        Janitor.ax1.plot(Janitor.tlist, Janitor.fourlist, label="4", color=Janitor.colors[4])
        Janitor.ax1.plot(Janitor.tlist, Janitor.fivelist, label="5", color=Janitor.colors[5])
        Janitor.ax1.plot(Janitor.tlist, Janitor.sixlist, label="6", color=Janitor.colors[6])
        h = Janitor.ax2.imshow(defheatmap, cmap=Janitor.cm)
        fig.colorbar(h, cmap=Janitor.cm)
        for n in range(0, 7):
            defheatmap[0, n] = 0
        Janitor.ax2.imshow(defheatmap, cmap=Janitor.cm)
        Janitor.ax1.legend(loc='upper left')
        Janitor.ax1.set_title('The number of cell type')
        Janitor.ax2.set_title('Cell simuration')


    @classmethod
    def plot_heatmap_graph(cls):
        Janitor.ax1.plot(Janitor.tlist, Janitor.threelist, label="3", color=Janitor.colors[3])
        Janitor.ax1.plot(Janitor.tlist, Janitor.fourlist, label="4", color=Janitor.colors[4])
        Janitor.ax1.plot(Janitor.tlist, Janitor.fivelist, label="5", color=Janitor.colors[5])
        Janitor.ax1.plot(Janitor.tlist, Janitor.sixlist, label="6", color=Janitor.colors[6])
        Janitor.ax2.imshow(Janitor.heatmap,interpolation="nearest", cmap=Janitor.cm)
        plt.pause(0.05)

    @classmethod
    def count_cell_num(cls):
        Janitor.n = np.sum(Janitor.field > -1)

    @classmethod
    def append_cell_num(cls):
        Janitor.threelist.append(np.sum(Janitor.heatmap == 3))
        Janitor.fourlist.append(np.sum(Janitor.heatmap == 4))
        Janitor.fivelist.append(np.sum(Janitor.heatmap == 5))
        Janitor.sixlist.append(np.sum(Janitor.heatmap == 6))
        Janitor.tlist.append(Janitor.t)

    @classmethod
    def count(cls):
        for n in range(3, 7):
            print("cell{}:{}個".format(n, np.sum(Janitor.heatmap == n)))

    @classmethod
    def refresh_heatmap(cls):
        Janitor.heatmap = np.zeros((Janitor.SIZE, Janitor.SIZE))
