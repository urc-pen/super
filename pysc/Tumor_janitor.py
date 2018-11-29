from Janitor import Janitor
import numpy as np
import random
import math
import fractions
import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
import matplotlib.animation as animation

class Tumor_janitor(Janitor):
    @classmethod
    def receive_value(cls, func, SIZE, MAXNUM, INTERVAL):
        super().receive_value(func, SIZE, MAXNUM, INTERVAL)
        Janitor.t = 0
        Janitor.tlist =[]
        Janitor.onelist = []
        Janitor.twolist = []
        Janitor.ims = []

    @classmethod
    def create_value(cls, mode):
        if mode == "drug":
            Janitor.mode = "drug"
            Janitor.colors = [(1, 1, 1), (0.2, 0.8, 1), (0.8, 0.1, 0.2)]
            Janitor.label1 = "1: no Drug-resistant"
            Janitor.label2 = "2: Drug-resistant mutations"
        if mode == "driver":
            Janitor.mode = "driver"
            Janitor.colors = [(1, 1, 1), (0.2, 0.8, 1), (0.5, 0.8, 0.2)]
            Janitor.label1 = "1: no mutation"
            Janitor.label2 = "2: driver mutation"

    @classmethod
    def receive_field_heatmap(cls, field, heatmap):
        Janitor.field = field
        Janitor.heatmap = heatmap

    @classmethod
    def append_cell_num(cls):
        n1 = np.sum(Janitor.heatmap == 1)
        n2 = np.sum(Janitor.heatmap == 2)
        n1 += 1
        n2 += 1
        Janitor.onelist.append(n1)
        Janitor.twolist.append(n2)
        Janitor.tlist.append(Janitor.t)

    @classmethod
    def first_heatmap_graph(cls, append=False):
        Janitor.fig = plt.figure(figsize=(10, 5))
        cmap_name = 'my_list'
        Janitor.cm = LinearSegmentedColormap.from_list(cmap_name, Janitor.colors, N=3)
        Janitor.ax1 = Janitor.fig.add_subplot(1, 2, 1)
        Janitor.ax2 = Janitor.fig.add_subplot(1, 2, 2)
        Janitor.ax1.set_yscale('log')
        Janitor.ax1.set_ylim([1,1000000])
        im = Janitor.ax1.plot(Janitor.tlist, Janitor.onelist, label=Janitor.label1, color=Janitor.colors[1])
        im += Janitor.ax1.plot(Janitor.tlist, Janitor.twolist, label=Janitor.label2, color=Janitor.colors[2])
        defheatmap = Janitor.heatmap
        for n in range(0, 3):
            defheatmap[0, n] = n
        h = Janitor.ax2.imshow(defheatmap, cmap=Janitor.cm)
        Janitor.fig.colorbar(h, cmap=Janitor.cm)
        for n in range(0, 3):
            defheatmap[0, n] = 0
        h2 = Janitor.ax2.imshow(defheatmap, cmap=Janitor.cm)
        im += [h2]
        Janitor.ax1.legend(loc='lower right', bbox_to_anchor=(1.8,-0.1))
        Janitor.ax1.set_title('The number of cell type')
        Janitor.ax2.set_title('Cell simuration')
        if append == True:
            Janitor.ims.append(im)

    @classmethod
    def plot_append_heatmap_graph(cls, plot=True, append=False):
        if plot == True or append == True:
            for n in range(1, 3):
                Janitor.heatmap[0, n - 1] = n
            im = Janitor.ax1.plot(Janitor.tlist, Janitor.onelist, label=Janitor.label1, color=Janitor.colors[1])
            im += Janitor.ax1.plot(Janitor.tlist, Janitor.twolist, label=Janitor.label2, color=Janitor.colors[2])
            h = Janitor.ax2.imshow(Janitor.heatmap,interpolation="nearest", cmap=Janitor.cm)
            im += [h]
            if plot == True:
                plottime = Janitor.t % Janitor.INTERVAL
                if plottime == 0:
                    plt.pause(0.01)
            if append == True:
                Janitor.ims.append(im)
        else:
            pass

    @classmethod
    def count(cls):
        for n in range(1, 3):
            print("cell{}:{}個".format(n, np.sum(Janitor.heatmap == n)))

    @classmethod
    def count_type(cls):
        Janitor.cell_one_num = np.sum(Janitor.heatmap == 1)
        Janitor.cell_two_num = np.sum(Janitor.heatmap == 2)

    @classmethod
    def save_heatmap_graph(cls, mode, para):
        if mode == "pic":
            for n in range(1, 3):
                Janitor.heatmap[0, n - 1] = n
            Janitor.ax1.plot(Janitor.tlist, Janitor.onelist, label=Janitor.label1, color=Janitor.colors[1])
            Janitor.ax1.plot(Janitor.tlist, Janitor.twolist, label=Janitor.label2, color=Janitor.colors[2])
            Janitor.ax2.imshow(Janitor.heatmap,interpolation="nearest", cmap=Janitor.cm)
            pidpng = "../result/pngstore/" + para + ".png"
            plt.savefig(pidpng)
        if mode == "anime":
            ani = animation.ArtistAnimation(Janitor.fig, Janitor.ims, interval=50, blit=True, repeat_delay=1000)
            pidgif = "../result/gifstore/" + para + ".gif"
            ani.save(pidgif, writer="imagemagick")
