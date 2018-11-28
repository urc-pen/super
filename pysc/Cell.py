import numpy as np
import random
import math
import fractions
import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap

class Cell:
    num = 0
    celllist = []
    @classmethod
    def receive_value(cls, AVERAGE, DISPERSION, ENV):
        Cell.AVERAGE = AVERAGE
        Cell.DISPERSION = DISPERSION
        Cell.ENV = ENV

    def __init__(self, i, j):
        self.i = i
        self.j = j
        self.id = 0
        self.type = 0
        self.waittime = 0
        self.count = 0
        self.proliferation = 0
        self.dead = 0
        self.num = 0
        self.deathflag = 0

    @classmethod
    def set_first_cell(cls, field, on):
        first_cell = Cell(on, on)
        first_cell.id = 0
        first_cell.type = 0
        first_cell.waittime = 1
        first_cell.count = 0
        first_cell.proliferation = 0
        Cell.celllist.append(first_cell)
        field[first_cell.i, first_cell.j] = first_cell.id

    def dire1(self, field):
        direction = random.randint(0,7)
        if direction == 0:
            Cell.mi = -1
            Cell.mj = -1
        if direction == 1:
            Cell.mi = -1
            Cell.mj = 0
        if direction == 2:
            Cell.mi = -1
            Cell.mj = 1
        if direction == 3:
            Cell.mi = 0
            Cell.mj = -1
        if direction == 4:
            Cell.mi = 0
            Cell.mj = 1
        if direction == 5:
            Cell.mi = 1
            Cell.mj = -1
        if direction == 6:
            Cell.mi = 1
            Cell.mj = 0
        if direction == 7:
            Cell.mi = 1
            Cell.mj = 1

    def dire2(self, field):
        obstacle_num = []
        for mi in range(-1, 2):
            for mj in range(-1, 2):
                if mi == 0 and mj == 0:
                    continue
                ni = self.i + mi
                nj = self.j + mj
                id = field[self.i, self.j]
                proposi = field[ni, nj]
                if proposi == -1:
                    obstacle_num.append(1)
                else:
                    while proposi != -1:
                        obstacle = 1
                        obstacle += 1
                        ni += mi
                        nj += mj
                        proposi = field[ni, nj]
                    if proposi == -1:
                        obstacle_num.append(obstacle)
        obstacle_ratio = []
        for i in range(0, 8):
            if obstacle_num[i] == 0:
                obstacle_ratio.append(0)
            else:
                obstacle_ratio.append(fractions.Fraction(1, obstacle_num[i]))
        obstacle_sum = sum(obstacle_ratio)
        dire_ratio = []
        for i in range(0, 8):
            if obstacle_ratio[i] == 0:
                dire_ratio.append(0)
            else:
                dire_ratio.append(fractions.Fraction(obstacle_ratio[i], obstacle_sum))

        if sum(dire_ratio) == 1:
            direction = np.random.choice([0,1,2,3,4,5,6,7], p=dire_ratio)
            if direction == 0:
                Cell.mi = -1
                Cell.mj = -1
            if direction == 1:
                Cell.mi = -1
                Cell.mj = 0
            if direction == 2:
                Cell.mi = -1
                Cell.mj = 1
            if direction == 3:
                Cell.mi = 0
                Cell.mj = -1
            if direction == 4:
                Cell.mi = 0
                Cell.mj = 1
            if direction == 5:
                Cell.mi = 1
                Cell.mj = -1
            if direction == 6:
                Cell.mi = 1
                Cell.mj = 0
            if direction == 7:
                Cell.mi = 1
                Cell.mj = 1

    def prolife(self, field):
        ni = self.i + Cell.mi
        nj = self.j + Cell.mj
        cell_new = Cell(ni, nj)
        cell_new.id = len(Cell.celllist)
        self.count += 1
        cell_new.count = self.count
        self.proliferation = 0
        if self.type <= 2:
            cell_new.type = int(self.type * 2 + 2)
            self.type = int(self.type * 2 + 1)
        elif self.type > 2:
            cell_new.type = self.type
        else:
            pass
        cell_new.move(field)
        Cell.celllist.append(cell_new)

    def move(self, field):
        ni = self.i + Cell.mi
        nj = self.j + Cell.mj
        if field[self.i, self.j] >= 0:
            id = field[self.i, self.j]
            Cell.celllist[id].i = ni
            Cell.celllist[id].j = nj
            Cell.celllist[id].move(field)
            field[self.i, self.j] = self.id
        else:
            field[self.i, self.j] = self.id

    @classmethod
    def radial_prolife(cls, field, on, func):
        if Cell.celllist[field[on, on]].proliferation == 1 and field[on, on] != -1:
            getattr(Cell.celllist[field[on, on]], func)(field)
            Cell.celllist[field[on, on]].prolife(field)
        for r in range(0, on):
            for k in range(0, 2 * r):
                if Cell.celllist[field[on - r, on - r + k]].proliferation == 1 and field[on - r, on - r + k] != -1:
                    getattr(Cell.celllist[field[on - r, on - r + k]], func)(field)
                    Cell.celllist[field[on - r, on - r + k]].prolife(field)
            for k in range(0, 2 * r):
                if Cell.celllist[field[on - r + k, on + r]].proliferation == 1 and field[on - r + k, on + r] != -1:
                    getattr(Cell.celllist[field[on - r + k, on + r]], func)(field)
                    Cell.celllist[field[on - r + k, on + r]].prolife(field)
            for k in range(0, 2 * r):
                if Cell.celllist[field[on + r, on + r - k]].proliferation == 1 and field[on + r, on + r - k] != -1:
                    getattr(Cell.celllist[field[on + r, on + r - k]], func)(field)
                    Cell.celllist[field[on + r, on + r - k]].prolife(field)
            for k in range(0, 2 * r):
                if Cell.celllist[field[on + r - k, on - r]].proliferation == 1 and field[on + r - k, on - r] != -1:
                    getattr(Cell.celllist[field[on + r - k, on - r]], func)(field)
                    Cell.celllist[field[on + r - k, on - r]].prolife(field)

    def waittime_gamma(self):
        if self.waittime == 0:
            SHAPE = Cell.AVERAGE ** 2 / Cell.DISPERSION
            SCALE = Cell.DISPERSION / Cell.AVERAGE
            self.waittime = math.ceil(np.random.gamma(SHAPE, SCALE))

    def decide_prolife(self):
        if self.waittime == 0:
            self.proliferation = 1

    def waittime_minus(self):
        if self.waittime != 0:
            self.waittime -= 1
            self.count += 1

    def update_heatmap(self, heatmap):
        if self.dead == 0:
            heatmap[self.i, self.j] = self.type

    @classmethod
    def countall(cls, heatmap):
        Cell.three_num = np.sum(heatmap == 3)
        Cell.four_num = np.sum(heatmap == 4)
        Cell.five_num = np.sum(heatmap == 5)
        Cell.six_num = np.sum(heatmap == 6)

    def count_around(self, r, heatmap):
        for i in range(self.i - r, self.i + r + 1):
            for j in range(self.j - r, self.j + r + 1):
                self.num = np.sum(heatmap[i, j] == self.type)

    def waittime_logistic(self):
        if self.num < Cell.ENV:
            self.waittime = np.round(self.waittime / (1 - self.num / Cell.ENV))
        elif self.num >= Cell.ENV:
            self.waittime = 2

    def mortal(self, num, field):
        if num < Cell.ENV and self.dead == 0:
            nE = num / Cell.ENV
            self.deathflag = np.random.choice([0, 1], p=[1 - nE, nE])
        if self.deathflag == 1:
            self.dead = 1
            field[self.i, self.j] = -1
            self.deathflag = 0
        else:
            pass

    def dead_or_alive(self, field):
        if self.type == 3:
            self.mortal(Cell.three_num, field)
        if self.type == 4:
            self.mortal(Cell.four_num, field)
        if self.type == 5:
            self.mortal(Cell.five_num, field)
        if self.type == 6:
            self.mortal(Cell.six_num, field)
