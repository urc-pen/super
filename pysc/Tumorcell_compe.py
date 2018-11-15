from Cell import Cell
import numpy as np
import random
import math
import fractions
import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
from decimal import *

class Tumor_cell_compe(Cell):

    @classmethod
    def receive_value(cls, AVERAGE, DISPERSION, AROUND, WEIGHT1, WEIGHT2, MTRATE, DRUGTIMES, EFFECT):
        Cell.AVERAGE = AVERAGE
        Cell.DISPERSION = DISPERSION
        Cell.AROUND = AROUND
        Cell.WEIGHT1 = WEIGHT1
        Cell.WEIGHT2 = WEIGHT2
        Cell.MTRATE = MTRATE
        Cell.K1 = Cell.AVERAGE * 8 * Cell.AROUND * (Cell.AROUND + 1)
        Cell.K2 = Cell.AVERAGE * 8 * Cell.AROUND * (Cell.AROUND + 1) * (Cell.WEIGHT1 + 1)
        Cell.KM = (2 * Cell.AROUND + 1) ** 2 - 1
        Cell.EFFECT = EFFECT
        Cell.drtime_list = DRUGTIMES.split(",")
        Cell.resicount = 0

    @classmethod
    def receive_list(cls, list):
        Cell.celllist = list

    def __init__(self, i, j):
        super().__init__(i, j)
        self.mutation_id = 1
        self.resistflag = 0
        self.enemynum = 0
        self.type = 1
        self.drdeath = 0

    @classmethod
    def set_first_cell(cls, field, on):
        first_cell = Tumor_cell_compe(on, on)
        first_cell.id = 0
        first_cell.type = 1
        first_cell.waittime = 1
        first_cell.count = 0
        first_cell.proliferation = 0
        Cell.celllist.append(first_cell)
        field[first_cell.i, first_cell.j] = first_cell.id

    def prolife(self, field):
        ni = self.i + Cell.mi
        nj = self.j + Cell.mj
        cell_new = Tumor_cell_compe(ni, nj)
        cell_new.id = len(Cell.celllist)
        self.count += 1
        cell_new.mutation_id = self.mutation_id * 2 + 1
        self.mutation_id = self.mutation_id * 2
        cell_new.count = self.count
        self.proliferation = 0
        cell_new.type = self.type

        if self.type == 1:
            self.resistflag = np.random.choice([1, 0], p=[Cell.MTRATE, 1 - Cell.MTRATE])
            if self.resistflag == 1:
                Cell.resicount += 1
                self.type = 2
                self.resistflag = 0

        cell_new.move(field)
        Cell.celllist.append(cell_new)

    @classmethod
    def radial_prolife(cls, field, on, func):
        if Cell.celllist[field[on, on]].proliferation == 1:
            getattr(Cell.celllist[field[on, on]], func)(field)
            Cell.celllist[field[on, on]].prolife(field)
        for r in range(0, on):
            for k in range(0, 2 * r):
                if Cell.celllist[field[on - r, on - r + k]].proliferation == 1:
                    getattr(Cell.celllist[field[on - r, on - r + k]], func)(field)
                    Cell.celllist[field[on - r, on - r + k]].prolife(field)
            for k in range(0, 2 * r):
                if Cell.celllist[field[on - r + k, on + r]].proliferation == 1:
                    getattr(Cell.celllist[field[on - r + k, on + r]], func)(field)
                    Cell.celllist[field[on - r + k, on + r]].prolife(field)
            for k in range(0, 2 * r):
                if Cell.celllist[field[on + r, on + r - k]].proliferation == 1:
                    getattr(Cell.celllist[field[on + r, on + r - k]], func)(field)
                    Cell.celllist[field[on + r, on + r - k]].prolife(field)
            for k in range(0, 2 * r):
                if Cell.celllist[field[on + r - k, on - r]].proliferation == 1:
                    getattr(Cell.celllist[field[on + r - k, on - r]], func)(field)
                    Cell.celllist[field[on + r - k, on - r]].prolife(field)

    def count_around(self, heatmap):
        self.num = 0
        self.enemynum = 0
        if self.dead == 0:
            arheatmap = heatmap[self.i - Cell.AROUND:self.i + Cell.AROUND + 1, self.j - Cell.AROUND:self.j + Cell.AROUND + 1].flatten()
            nozeroheat = arheatmap[arheatmap != 0]
            self.num = -1 + len(nozeroheat[nozeroheat == self.type])
            self.enemynum = len(nozeroheat[nozeroheat != self.type])

    def mortal1(self, field):
        if self.enemynum <= Cell.K1 and self.dead == 0:
            nE = (self.num + self.enemynum) / Cell.K2
            nE = round(nE, 3)
            self.deathflag = np.random.choice([0, 1], p=[1 - nE, nE])
        if self.deathflag == 1:
            self.dead = 1
            field[self.i, self.j] = -1
            self.deathflag = 0
        else:
            pass

    def mortal2(self, field):
        if self.dead == 0:
            if self.type == 1:
                nE = (self.num + self.enemynum * Cell.WEIGHT2) / Cell.K1
                nE = round(nE, 3)
            if self.type == 2:
                nE = (self.num + self.enemynum * Cell.WEIGHT1) / Cell.K1
                nE = round(nE, 3)
            self.deathflag = np.random.choice([0, 1], p=[1 - nE, nE])
        if self.deathflag == 1:
            self.dead = 1
            field[self.i, self.j] = -1
            self.deathflag = 0
        else:
            pass

    def drugged(self, t):
        if len(Cell.drtime_list) != 0 and self.dead == 0:
            if t >= int(Cell.drtime_list[0]) and t < int(Cell.drtime_list[1]):
                if self.type == 1:
                    dens = 1 - (self.num + self.enemynum) / Cell.KM
                    self.drdeath = dens * Cell.EFFECT
                else:
                    self.drdeath = 0
            if t == int(Cell.drtime_list[1]):
                if self.type == 1:
                    self.drdeath = 0

    @classmethod
    def drtime_list_adjust(cls, t):
        if len(Cell.drtime_list) != 0:
            if t == int(Cell.drtime_list[1]):
                del Cell.drtime_list[0:2]

    def mortal1_drug(self, field):
        if self.dead == 0:
            nE = (self.enemynum / Cell.K1) + self.drdeath
            if nE >= 1:
                nE = 1
            self.deathflag = np.random.choice([0, 1], p=[1 - nE, nE])
        if self.deathflag == 1:
            self.dead = 1
            field[self.i, self.j] = -1
            self.deathflag = 0
        else:
            pass

    def mortal2_drug(self, field):
        if self.dead == 0:
            nE = ((self.num * Cell.WEIGHT + self.enemynum) / Cell.K2) + self.drdeath
            if nE >= 1:
                nE = 1
            self.deathflag = np.random.choice([0, 1], p=[1 - nE, nE])
        if self.deathflag == 1:
            self.dead = 1
            field[self.i, self.j] = -1
            self.deathflag = 0
        else:
            pass
