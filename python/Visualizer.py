import numpy as np
import random
import math
import fractions
import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
import matplotlib.animation as animation

class Visualizer:

    def __init__(self):
        self.threelist = []
        self.fourlist = []
        self.fivelist = []
        self.sixlist = []
        self.tlist = []
        self.ims = []

    def receive_value(self, INTERVAL):
        self.INTERVAL = INTERVAL

    def append_cell_num(self, heatmap, t):
        self.threelist.append(np.sum(heatmap == 3) + 1)
        self.fourlist.append(np.sum(heatmap == 4) + 1)
        self.fivelist.append(np.sum(heatmap == 5) + 1)
        self.sixlist.append(np.sum(heatmap == 6) + 1)
        self.tlist.append(t)

    def first_heatmap_graph(self, heatmap):
        self.fig = plt.figure(figsize=(10, 5))
        self.colors = [(1, 1, 1), (0, 0.2, 0.8), (0, 0.3, 0.7) ,(0.5, 0, 0.5), (1, 0, 0), (0.2, 0.8, 1), (0.5, 0.8, 0.2)]
        cmap_name = 'my_list'
        self.cm = LinearSegmentedColormap.from_list(cmap_name, self.colors, N=7)
        defheatmap = heatmap
        for n in range(0, 7):
            defheatmap[0, n] = n
        self.ax1 = self.fig.add_subplot(1, 2, 1)
        self.ax2 = self.fig.add_subplot(1, 2, 2)
        self.ax1.set_yscale('log')
        self.ax1.set_ylim([1,1000000])
        self.ax1.plot(self.tlist, self.threelist, label="3", color=self.colors[3])
        self.ax1.plot(self.tlist, self.fourlist, label="4", color=self.colors[4])
        self.ax1.plot(self.tlist, self.fivelist, label="5", color=self.colors[5])
        self.ax1.plot(self.tlist, self.sixlist, label="6", color=self.colors[6])
        h = self.ax2.imshow(defheatmap, cmap=self.cm)
        self.fig.colorbar(h, cmap=self.cm)
        for n in range(0, 7):
            defheatmap[0, n] = 0
        self.ax2.imshow(defheatmap, cmap=self.cm)
        self.ax1.legend(loc='upper left')
        self.ax1.set_title('The number of cell type')
        self.ax2.set_title('Cell simuration')

    def plot_append_heatmap_graph(self, heatmap, t, plot=False, append=True):
            if plot == True or append == True:
                for n in range(0, 7):
                    heatmap[0, n] = n
                im = self.ax1.plot(self.tlist, self.threelist, label="3", color=self.colors[3])
                im += self.ax1.plot(self.tlist, self.fourlist, label="4", color=self.colors[4])
                im += self.ax1.plot(self.tlist, self.fivelist, label="5", color=self.colors[5])
                im += self.ax1.plot(self.tlist, self.sixlist, label="6", color=self.colors[6])
                h = self.ax2.imshow(heatmap,interpolation="nearest", cmap=self.cm)
                im += [h]
                if plot == True:
                    plottime = t % self.INTERVAL
                    if plottime == 0:
                        plt.pause(0.01)
                if append == True:
                    self.ims.append(im)
            else:
                pass

    def save_heatmap_graph(self, mode, para, heatmap):
        if mode == "pic":
            self.ax1.plot(self.tlist, self.threelist, label="3", color=self.colors[3])
            self.ax1.plot(self.tlist, self.fourlist, label="4", color=self.colors[4])
            self.ax1.plot(self.tlist, self.fivelist, label="5", color=self.colors[5])
            self.ax1.plot(self.tlist, self.sixlist, label="6", color=self.colors[6])
            self.ax2.imshow(heatmap,interpolation="nearest", cmap=self.cm)
            pidpng = "../result/pngstore/" + para + ".png"
            plt.savefig(pidpng)
        if mode == "anime":
            ani = animation.ArtistAnimation(self.fig, self.ims, interval=50, blit=True, repeat_delay=1000)
            pidgif = "../result/gifstore/" + para + ".gif"
            ani.save(pidgif, writer="imagemagick")
