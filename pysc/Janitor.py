import numpy as np
import random
import math
import fractions
import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
import matplotlib.animation as animation

class Janitor:

    cell_one_num = 0
    cell_two_num = 0
    ims = []

    @classmethod
    def receive_value(cls, func, SIZE, MAXNUM, INTERVAL):
        Janitor.func = func
        Janitor.SIZE = SIZE                    #フィールドの大きさ
        Janitor.on = int((Janitor.SIZE - 1) / 2)
        Janitor.t = 0
        Janitor.n = 0
        Janitor.MAXNUM = MAXNUM
        Janitor.INTERVAL = INTERVAL
        Janitor.threelist = []
        Janitor.fourlist = []
        Janitor.fivelist = []
        Janitor.sixlist = []
        Janitor.tlist = []

    @classmethod
    def set_field(cls):
        Janitor.field = np.full((Janitor.SIZE, Janitor.SIZE), -1, dtype=int)

    @classmethod
    def set_heatmap(cls):
        Janitor.heatmap = np.zeros((Janitor.SIZE, Janitor.SIZE))

    @classmethod
    def first_heatmap_graph(cls):
        Janitor.fig = plt.figure(figsize=(10, 5))
        Janitor.colors = [(1, 1, 1), (0, 0.2, 0.8), (0, 0.3, 0.7) ,(0.5, 0, 0.5), (1, 0, 0), (0.2, 0.8, 1), (0.5, 0.8, 0.2)]
        cmap_name = 'my_list'
        Janitor.cm = LinearSegmentedColormap.from_list(cmap_name, Janitor.colors, N=7)
        defheatmap = Janitor.heatmap
        for n in range(0, 7):
            defheatmap[0, n] = n
        Janitor.ax1 = Janitor.fig.add_subplot(1, 2, 1)
        Janitor.ax2 = Janitor.fig.add_subplot(1, 2, 2)
        Janitor.ax1.set_yscale('log')
        Janitor.ax1.set_ylim([1,130000])
        Janitor.ax1.plot(Janitor.tlist, Janitor.threelist, label="3", color=Janitor.colors[3])
        Janitor.ax1.plot(Janitor.tlist, Janitor.fourlist, label="4", color=Janitor.colors[4])
        Janitor.ax1.plot(Janitor.tlist, Janitor.fivelist, label="5", color=Janitor.colors[5])
        Janitor.ax1.plot(Janitor.tlist, Janitor.sixlist, label="6", color=Janitor.colors[6])
        h = Janitor.ax2.imshow(defheatmap, cmap=Janitor.cm)
        Janitor.fig.colorbar(h, cmap=Janitor.cm)
        for n in range(0, 7):
            defheatmap[0, n] = 0
        Janitor.ax2.imshow(defheatmap, cmap=Janitor.cm)
        Janitor.ax1.legend(loc='upper left')
        Janitor.ax1.set_title('The number of cell type')
        Janitor.ax2.set_title('Cell simuration')

    @classmethod
    def plot_append_heatmap_graph(cls, plot=True, append=False):
        plottime = Janitor.t % Janitor.INTERVAL
        if plottime == 0:
            if plot == True or append == True:
                im = Janitor.ax1.plot(Janitor.tlist, Janitor.threelist, label="3", color=Janitor.colors[3])
                im += Janitor.ax1.plot(Janitor.tlist, Janitor.fourlist, label="4", color=Janitor.colors[4])
                im += Janitor.ax1.plot(Janitor.tlist, Janitor.fivelist, label="5", color=Janitor.colors[5])
                im += Janitor.ax1.plot(Janitor.tlist, Janitor.sixlist, label="6", color=Janitor.colors[6])
                h = Janitor.ax2.imshow(Janitor.heatmap,interpolation="nearest", cmap=Janitor.cm)
                im += [h]
                if plot == True:
                    plt.pause(0.01)
                if append == True:
                    Janitor.ims.append(im)
            else:
                pass

    @classmethod
    def count_cell_num(cls):
        Janitor.n = np.sum(Janitor.field > -1)

    @classmethod
    def append_cell_num(cls):
        Janitor.threelist.append(np.sum(Janitor.heatmap == 3) + 1)
        Janitor.fourlist.append(np.sum(Janitor.heatmap == 4) + 1)
        Janitor.fivelist.append(np.sum(Janitor.heatmap == 5) + 1)
        Janitor.sixlist.append(np.sum(Janitor.heatmap == 6) + 1)
        Janitor.tlist.append(Janitor.t)

    @classmethod
    def count(cls):
        for n in range(3, 7):
            print("cell{}:{}個".format(n, np.sum(Janitor.heatmap == n)))

    @classmethod
    def refresh_heatmap(cls):
        Janitor.heatmap = np.zeros((Janitor.SIZE, Janitor.SIZE))

    @classmethod
    def save_heatmap_graph(cls, mode, para):
        if mode == "pic":
            Janitor.ax1.plot(Janitor.tlist, Janitor.threelist, label="3", color=Janitor.colors[3])
            Janitor.ax1.plot(Janitor.tlist, Janitor.fourlist, label="4", color=Janitor.colors[4])
            Janitor.ax1.plot(Janitor.tlist, Janitor.fivelist, label="5", color=Janitor.colors[5])
            Janitor.ax1.plot(Janitor.tlist, Janitor.sixlist, label="6", color=Janitor.colors[6])
            Janitor.ax2.imshow(Janitor.heatmap,interpolation="nearest", cmap=Janitor.cm)
            pidpng = "../result/pngstore/" + para + ".png"
            plt.savefig(pidpng)
        if mode == "anime":
            ani = animation.ArtistAnimation(Janitor.fig, Janitor.ims, interval=50, blit=True, repeat_delay=1000)
            pidgif = "../result/gifstore/" + para + ".gif"
            ani.save(pidgif, writer="imagemagick")
