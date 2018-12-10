import numpy as np
import random
import math
import fractions
import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
import matplotlib.animation as animation
from Visualizer import Visualizer

class Visualizer_two(Visualizer):

    def __init__(self, mode):
        self.ims = []
        if mode == "drug":
            self.mode = "drug"
            self.colors = [(1, 1, 1), (0.2, 0.8, 1), (0.8, 0.1, 0.2)]
            self.label1 = "1: no Drug-resistant"
            self.label2 = "2: Drug-resistant mutations"
        if mode == "driver":
            self.mode = "driver"
            self.colors = [(1, 1, 1), (0.2, 0.8, 1), (0.5, 0.8, 0.2)]
            self.label1 = "1: no driver mutation"
            self.label2 = "2: driver mutation"

    def first_heatmap_graph(self, heatmap, tlist, onelist, twolist):
        self.fig = plt.figure(figsize=(10, 5))
        cmap_name = 'my_list'
        self.cm = LinearSegmentedColormap.from_list(cmap_name, self.colors, N=3)
        defheatmap = heatmap
        for n in range(0, 3):
            defheatmap[0, n] = n
        self.ax1 = self.fig.add_subplot(1, 2, 1)
        self.ax2 = self.fig.add_subplot(1, 2, 2)
        self.ax1.set_yscale('log')
        self.ax1.set_ylim([1,1000000])
        self.ax1.plot(tlist, onelist, label=self.label1, color=self.colors[1])
        self.ax1.plot(tlist, twolist, label=self.label2, color=self.colors[2])
        h = self.ax2.imshow(defheatmap, cmap=self.cm)
        self.fig.colorbar(h, cmap=self.cm)
        for n in range(0, 3):
            defheatmap[0, n] = n
        self.ax2.imshow(defheatmap, cmap=self.cm)
        self.ax1.legend(loc='lower right', bbox_to_anchor=(1.8,-0.1))
        self.ax1.set_title('The number of cell type')
        self.ax2.set_title('Cell simuration')

    def plot_append_heatmap_graph(self, heatmap, t, tlist, onelist, twolist, plot=False, append=True):
            if plot == True or append == True:
                for n in range(0, 3):
                    heatmap[0, n] = n
                im = self.ax1.plot(tlist, onelist, label=self.label1, color=self.colors[1])
                im += self.ax1.plot(tlist, twolist, label=self.label2, color=self.colors[2])
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

    def save_heatmap_graph(self, mode, para, heatmap, tlist, onelist, twolist, fname):
        if mode == "pic":
            self.ax1.plot(tlist, onelist, label=self.label1, color=self.colors[1])
            self.ax1.plot(tlist, twolist, label=self.label2, color=self.colors[2])
            self.ax2.imshow(heatmap,interpolation="nearest", cmap=self.cm)
            pidpng = fname + "/pngstore/" + para + ".png"
            plt.savefig(pidpng)
        if mode == "anime":
            ani = animation.ArtistAnimation(self.fig, self.ims, interval=50, blit=True, repeat_delay=1000)
            pidgif = fname + "/gifstore/" + para + ".gif"
            ani.save(pidgif, writer="imagemagick")
