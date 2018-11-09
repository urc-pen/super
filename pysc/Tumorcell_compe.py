from Cell import Cell
import numpy as np
import random
import math
import fractions
import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap

class Tumor_cell_compe(Cell):

    @classmethod
    def receive_value(cls,AVERAGE, DISPERSION, ENV, AROUND, WEIGHT):
        super().receive_value(AVERAGE, DISPERSION, ENV)
        Cell.AROUND = AROUND
        Cell.WEIGHT = WEIGHT

    def __init__(self, i, j):
        super().__init__(i, j)
        self.driver_mutation = 0
        self.mutation_id = 1
        self.driverflag = 0
        self.enemynum = 0

    @classmethod
    def set_first_cell(cls, field, on):
        first_cell = Tumor_cell_compe(on, on)
        first_cell.id = 0
        first_cell.type = 0
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

        if self.type == 0:
            self.type = 1
            cell_new.type = 2

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
        for i in range(self.i - Cell.AROUND, self.i + Cell.AROUND + 1):
            for j in range(self.j - Cell.AROUND, self.j + Cell.AROUND + 1):
                if i == self.i and j == self.j:
                    continue
                bool = (heatmap[i, j] == self.type)
                enemybool = (heatmap[i, j] != self.type and heatmap[i, j] != 0)
                self.num += bool
                self.enemynum += enemybool

    def mortal1(self, field):
        K = (Cell.AROUND * 2 + 1) ** 2 - 1
        K = 1000
        if self.enemynum < K and self.dead == 0:
            nE = self.enemynum / K
            self.deathflag = np.random.choice([0, 1], p=[1 - nE, nE])
        if self.deathflag == 1:
            self.dead = 1
            field[self.i, self.j] = -1
            self.deathflag = 0
        else:
            pass

    def mortal2(self, field):
        K = (Cell.AROUND * 2 + 1) ** 2 - 1
        K = 1000
        if self.enemynum < K and self.dead == 0:
            nE = (self.num * Cell.WEIGHT + self.enemynum) / K
            self.deathflag = np.random.choice([0, 1], p=[1 - nE, nE])
        if self.deathflag == 1:
            self.dead = 1
            field[self.i, self.j] = -1
            self.deathflag = 0
        else:
            pass
