from Cell import Cell
import numpy as np
import random
import math
import fractions
import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
from decimal import *

class Cell_compe(Cell):
    @classmethod
    def receive_value(cls, AVERAGE, DISPERSION, AROUND, WEIGHT):
        Cell.AVERAGE = AVERAGE
        Cell.DISPERSION = DISPERSION
        Cell.AROUND = AROUND
        Cell.WEIGHT = WEIGHT
        Cell.K = Cell.AVERAGE * 8 * Cell.AROUND * (Cell.AROUND + 1)
        Cell.KM = (2 * Cell.AROUND + 1) ** 2 - 1

    def __init__(self, i, j):
        super().__init__(i, j)
        self.mutation_id = 1
        self.resistflag = 0
        self.enemynum = 0
        self.type = 1
        self.drdeath = 0
        self.driver_mutation = 0
        self.driverflag = 0
        self.driver_type = 0

    @classmethod
    def set_first_cell(cls, field, on, celllist):
        first_cell = Cell_compe(on, on)
        first_cell.id = 0
        first_cell.type = 0
        first_cell.waittime = 1
        first_cell.count = 0
        first_cell.proliferation = 0
        celllist.append(first_cell)
        field[first_cell.i, first_cell.j] = first_cell.id

    def prolife(self, field, celllist, timedic):
        ni = self.i + Cell.mi
        nj = self.j + Cell.mj
        cell_new = Cell_compe(ni, nj)
        cell_new.id = len(celllist)
        cell_new.mutation_id = self.mutation_id * 2 + 1
        self.mutation_id = self.mutation_id * 2
        timedic[self.mutation_id] = self.count
        timedic[cell_new.mutation_id] = self.count
        self.count = 0
        self.proliferation = 0
        cell_new.driver_mutation = self.driver_mutation
        if self.type <= 2:
            cell_new.type = int(self.type * 2 + 2)
            self.type = int(self.type * 2 + 1)
        elif self.type > 2:
            cell_new.type = self.type
        else:
            pass
        cell_new.move(field, celllist)
        celllist.append(cell_new)

    def prolife_simple(self, field, cellist):
        ni = self.i + Cell.mi
        nj = self.j + Cell.mj
        cell_new = Cell_compe(ni, nj)
        cell_new.id = len(celllist)
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

        cell_new.move(field, celllist)
        celllist.append(cell_new)

    @classmethod
    def radial_prolife_up(cls, field, on, func, celllist, timedic):
        if celllist[field[on, on]].proliferation == 1:
            getattr(celllist[field[on, on]], func)(field)
            celllist[field[on, on]].prolife(field, celllist, timedic)
        for r in range(1, on):
            a = field[on - r, on - r : on + r + 1].flatten()
            a = list(a[a != -1])
            for i in a:
                if celllist[i].proliferation == 1:
                    getattr(celllist[i], func)(field)
                    celllist[i].prolife(field, celllist, timedic)
            b = field[on - r + 1 : on + r + 1, on + r].flatten()
            b = list(b[b != -1])
            for i in b:
                if celllist[i].proliferation == 1:
                    getattr(celllist[i], func)(field)
                    celllist[i].prolife(field, celllist, timedic)
            c = field[on + r, on + r - 1: on - r -1 : -1].flatten()
            c = list(c[c != -1])
            for i in c:
                if celllist[i].proliferation == 1:
                    getattr(celllist[i], func)(field)
                    celllist[i].prolife(field, celllist, timedic)
            d = field[on + r - 1 : on - r : -1, on - r].flatten()
            d = list(d[d != -1])
            for i in d:
                if celllist[i].proliferation == 1:
                    getattr(celllist[i], func)(field)
                    celllist[i].prolife(field, celllist, timedic)

    def count_around(self, heatmap):
        self.num = 0
        self.enemynum = 0
        if self.dead == 0:
            arheatmap = heatmap[self.i - Cell.AROUND:self.i + Cell.AROUND + 1, self.j - Cell.AROUND:self.j + Cell.AROUND + 1].flatten()
            nozeroheat = arheatmap[arheatmap != 0]
            self.num = -1 + len(nozeroheat[nozeroheat == self.type])
            self.enemynum = len(nozeroheat[nozeroheat != self.type])

    def mortal1(self, field):
        if self.enemynum <= Cell.K and self.dead == 0:
            nE = (self.num + self.enemynum) / Cell.K
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
            nE = (self.num + self.enemynum * Cell.WEIGHT) / Cell.K
            nE = round(nE, 3)
            self.deathflag = np.random.choice([0, 1], p=[1 - nE, nE])
        if self.deathflag == 1:
            self.dead = 1
            field[self.i, self.j] = -1
            self.deathflag = 0
        else:
            pass
