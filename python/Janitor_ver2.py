import numpy as np
import random
import math
import fractions
import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
import matplotlib.animation as animation

class Janitor:
    def __init__(self, mode):
        if mode == "two":
            self.mode = "two"
            self.cell_one_num = 0
            self.cell_two_num = 0
            self.onelist = []
            self.twolist = []
        if mode == "six":
            self.mode = "six"
            self.threelist = []
            self.fourlist = []
            self.fivelist = []
            self.sixlist = []
        self.tlist = []
        self.t = 0
        self.n = 0
        self.celllist = []
        self.timedic = {}
        self.driver_list = []

    def receive_value(self, func, SIZE, MAXNUM):
        self.func = func
        self.SIZE = SIZE                    #フィールドの大きさ
        self.on = int((self.SIZE - 1) / 2)
        self.MAXNUM = MAXNUM

    def set_field(self):
        self.field = np.full((self.SIZE, self.SIZE), -1, dtype=int)

    def set_heatmap(self):
        self.heatmap = np.zeros((self.SIZE, self.SIZE))

    def append_cell_num(self):
        if self.mode == "two":
            self.onelist.append(np.sum(self.heatmap == 1) + 1)
            self.twolist.append(np.sum(self.heatmap == 2) + 1)
        if self.mode == "six":
            self.threelist.append(np.sum(self.heatmap == 3) + 1)
            self.fourlist.append(np.sum(self.heatmap == 4) + 1)
            self.fivelist.append(np.sum(self.heatmap == 5) + 1)
            self.sixlist.append(np.sum(self.heatmap == 6) + 1)
        self.tlist.append(self.t)

    def count_cell_num(self):
        self.n = np.sum(self.field > -1)

    def count(self):
        for n in range(3, 7):
            print("cell{}:{}個".format(n, np.sum(self.heatmap == n)))


    def refresh_heatmap(self):
        self.heatmap = np.zeros((self.SIZE, self.SIZE))

    def list_adjust(self):
        self.driver_list.sort()

    def make_idlist(self):
        self.idlist = []
        refid = np.random.choice(self.field[self.field > -1], 256, replace=False)
        for i in refid:
            self.idlist.append(self.celllist[i].mutation_id)

    def make_idlist_includedead(self):
        self.idlist = []
        id = list(range(len(self.celllist)))
        refid = np.random.choice(id, 256, replace=False)
        for i in refid:
            self.idlist.append(self.celllist[i].mutation_id)

    def count_type(self):
        self.cell_one_num = np.sum(self.heatmap == 1)
        self.cell_two_num = np.sum(self.heatmap == 2)
