from Janitor import Janitor
import numpy as np
import random
import math
import fractions
import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap

class Tumor_janitor(Janitor):
    @classmethod
    def receive_value(cls, func, SIZE, MAXNUM, INTERVAL):
        super().receive_value(func, SIZE, MAXNUM)
        Janitor.t = 3
        Janitor.onelist = [0]
        Janitor.twolist = [0]
        Janitor.INTERVAL = INTERVAL

    @classmethod
    def receive_value_drug(cls, func, SIZE, MAXNUM, INTERVAL):
        super().receive_value(func, SIZE, MAXNUM)
        Janitor.t = 0
        Janitor.tlist = []
        Janitor.onelist = []
        Janitor.twolist = []
        Janitor.INTERVAL = INTERVAL

    @classmethod
    def receive_field_heatmap(cls, field, heatmap):
        Janitor.field = field
        Janitor.heatmap = heatmap

    @classmethod
    def append_cell_num(cls):
        Janitor.onelist.append(np.sum(Janitor.heatmap == 1))
        Janitor.twolist.append(np.sum(Janitor.heatmap == 2))
        Janitor.tlist.append(Janitor.t)

    @classmethod
    def first_heatmap_graph(cls):
        fig = plt.figure(figsize=(10, 5))
        Janitor.colors = [(1, 1, 1), (0.2, 0.8, 1), (0.5, 0.8, 0.2)]
        cmap_name = 'my_list'
        Janitor.cm = LinearSegmentedColormap.from_list(cmap_name, Janitor.colors, N=3)
        defheatmap = Janitor.heatmap
        for n in range(0, 3):
            defheatmap[0, n] = n
        Janitor.ax1 = fig.add_subplot(1, 2, 1)
        Janitor.ax2 = fig.add_subplot(1, 2, 2)
        Janitor.ax1.plot(Janitor.tlist, Janitor.onelist, label="1: no mutation", color=Janitor.colors[1])
        Janitor.ax1.plot(Janitor.tlist, Janitor.twolist, label="2: driver mutation", color=Janitor.colors[2])
        h = Janitor.ax2.imshow(defheatmap, cmap=Janitor.cm)
        fig.colorbar(h, cmap=Janitor.cm)
        for n in range(0, 3):
            defheatmap[0, n] = 0
        Janitor.ax2.imshow(defheatmap, cmap=Janitor.cm)
        Janitor.ax1.legend(loc='upper left')
        Janitor.ax1.set_title('The number of cell type')
        Janitor.ax2.set_title('Cell simuration')

    @classmethod
    def first_heatmap_graph_compe(cls):
        fig = plt.figure(figsize=(10, 5))
        Janitor.colors = [(1, 1, 1), (0.2, 0.8, 1), (0.5, 0.8, 0.2)]
        cmap_name = 'my_list'
        Janitor.cm = LinearSegmentedColormap.from_list(cmap_name, Janitor.colors, N=3)
        defheatmap = Janitor.heatmap
        for n in range(0, 3):
            defheatmap[0, n] = n
        Janitor.ax1 = fig.add_subplot(1, 2, 1)
        Janitor.ax2 = fig.add_subplot(1, 2, 2)
        Janitor.ax1.plot(Janitor.tlist, Janitor.onelist, label="1: no mutations", color=Janitor.colors[1])
        Janitor.ax1.plot(Janitor.tlist, Janitor.twolist, label="2: Drug-resistant mutations", color=Janitor.colors[2])
        h = Janitor.ax2.imshow(defheatmap, cmap=Janitor.cm)
        fig.colorbar(h, cmap=Janitor.cm)
        for n in range(0, 3):
            defheatmap[0, n] = 0
        Janitor.ax2.imshow(defheatmap, cmap=Janitor.cm)
        Janitor.ax1.legend(loc='upper left')
        Janitor.ax1.set_title('The number of cell type')
        Janitor.ax2.set_title('Cell simuration')

    @classmethod
    def inherit_heatmap_graph(cls):
        fig = plt.figure(figsize=(10, 5))
        Janitor.colors = [(1, 1, 1), (0.2, 0.8, 1), (0.5, 0.8, 0.2)]
        cmap_name = 'my_list'
        Janitor.cm = LinearSegmentedColormap.from_list(cmap_name, Janitor.colors, N=3)
        Janitor.ax1 = fig.add_subplot(1, 2, 1)
        Janitor.ax2 = fig.add_subplot(1, 2, 2)
        Janitor.ax1.plot(Janitor.tlist, Janitor.onelist, label="1: no mutations", color=Janitor.colors[1])
        Janitor.ax1.plot(Janitor.tlist, Janitor.twolist, label="2: Drug-resistant mutations", color=Janitor.colors[2])
        h = Janitor.ax2.imshow(Janitor.heatmap, cmap=Janitor.cm)
        fig.colorbar(h, cmap=Janitor.cm)
        Janitor.ax2.imshow(Janitor.heatmap, cmap=Janitor.cm)
        Janitor.ax1.legend(loc='upper left')
        Janitor.ax1.set_title('The number of cell type')
        Janitor.ax2.set_title('Cell simuration')


    @classmethod
    def plot_heatmap_graph(cls):
        plottime = Janitor.t % Janitor.INTERVAL
        if plottime == 0:
            for n in range(1, 3):
                Janitor.heatmap[0, n - 1] = n
            Janitor.ax1.plot(Janitor.tlist, Janitor.onelist, label="1: no mutation", color=Janitor.colors[1])
            Janitor.ax1.plot(Janitor.tlist, Janitor.twolist, label="2: driver mutation", color=Janitor.colors[2])
            Janitor.ax2.imshow(Janitor.heatmap,interpolation="nearest", cmap=Janitor.cm)
            plt.pause(0.01)

    @classmethod
    def plot_heatmap_graph_compe(cls):
        plottime = Janitor.t % Janitor.INTERVAL
        if plottime == 0:
            for n in range(1, 3):
                Janitor.heatmap[0, n - 1] = n
            Janitor.ax1.plot(Janitor.tlist, Janitor.onelist, label="1: no mutations", color=Janitor.colors[1])
            Janitor.ax1.plot(Janitor.tlist, Janitor.twolist, label="2: Drug-resistant mutations", color=Janitor.colors[2])
            Janitor.ax2.imshow(Janitor.heatmap,interpolation="nearest", cmap=Janitor.cm)
            plt.pause(0.01)

    @classmethod
    def count(cls):
        for n in range(1, 3):
            print("cell{}:{}個".format(n, np.sum(Janitor.heatmap == n)))

    @classmethod
    def save_heatmap_graph(cls, para):
        for n in range(1, 3):
            Janitor.heatmap[0, n - 1] = n
        Janitor.ax1.plot(Janitor.tlist, Janitor.onelist, label="1: no mutation", color=Janitor.colors[1])
        Janitor.ax1.plot(Janitor.tlist, Janitor.twolist, label="2: driver mutation", color=Janitor.colors[2])
        Janitor.ax2.imshow(Janitor.heatmap,interpolation="nearest", cmap=Janitor.cm)
        pidpng = "../result/pngstore/" + para + ".png"
        plt.savefig(pidpng)
