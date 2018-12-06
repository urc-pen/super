from Cell import Cell
import numpy as np
import random
import math
import fractions
import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
from decimal import *

class Tumor_cell(Cell):
    dr_type = 0
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
        Cell.DR_STRTIME = 0
        Cell.DR_DURATION = int(Cell.drtime_list[0])
        Cell.DR_INTERVAL = int(Cell.drtime_list[1])

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
        first_cell = Tumor_cell(on, on)
        first_cell.id = 0
        first_cell.type = 1
        first_cell.waittime = 1
        first_cell.count = 0
        first_cell.proliferation = 0
        celllist.append(first_cell)
        field[first_cell.i, first_cell.j] = first_cell.id

    def prolife(self, field, celllist, timedic, driver_list):
        ni = self.i + Cell.mi
        nj = self.j + Cell.mj
        cell_new = Tumor_cell(ni, nj)
        cell_new.id = len(celllist)
        cell_new.mutation_id = self.mutation_id * 2 + 1
        self.mutation_id = self.mutation_id * 2
        timedic[self.mutation_id] = self.count
        timedic[cell_new.mutation_id] = self.count
        self.count = 0
        self.proliferation = 0
        cell_new.driver_mutation = self.driver_mutation
        cell_new.type = self.type
        cell_new.driver_type = self.driver_type

        if self.driver_mutation == 0 and self.type == 1:
            self.driverflag = np.random.choice([1, 0], p=[Cell.MTRATE, 1 - Cell.MTRATE])
            if self.driverflag == 1:
                self.type = 2
                self.driver_mutation = 1
                driver_list.append(self.mutation_id)
                Tumor_cell.dr_type += 1
                self.driver_type = Tumor_cell.dr_type
                self.driverflag = 0
        else:
            pass

        if cell_new.driver_mutation == 0 and cell_new.type == 1:
            cell_new.driverflag = np.random.choice([1, 0], p=[Cell.MTRATE, 1 - Cell.MTRATE])
            if cell_new.driverflag == 1:
                cell_new.type = 2
                cell_new.driver_mutation = 1
                driver_list.append(cell_new.mutation_id)
                Tumor_cell.dr_type += 1
                cell_new.driver_type = Tumor_cell.dr_type
                cell_new.driverflag = 0
        else:
            pass

        cell_new.move(field, celllist)
        celllist.append(cell_new)

    def prolife_simple(self, field, celllist):
        ni = self.i + Cell.mi
        nj = self.j + Cell.mj
        cell_new = Tumor_cell(ni, nj)
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
    def radial_prolife_up(cls, field, on, func, celllist, timedic, driver_list):
        if celllist[field[on, on]].proliferation == 1:
            getattr(celllist[field[on, on]], func)(field)
            celllist[field[on, on]].prolife(field, celllist, timedic, driver_list)
        for r in range(1, on):
            a = field[on - r, on - r : on + r + 1].flatten()
            a = list(a[a != -1])
            for i in a:
                if celllist[i].proliferation == 1:
                    getattr(celllist[i], func)(field)
                    celllist[i].prolife(field, celllist, timedic, driver_list)
            b = field[on - r + 1 : on + r + 1, on + r].flatten()
            b = list(b[b != -1])
            for i in b:
                if celllist[i].proliferation == 1:
                    getattr(celllist[i], func)(field)
                    celllist[i].prolife(field, celllist, timedic, driver_list)
            c = field[on + r, on + r - 1: on - r -1 : -1].flatten()
            c = list(c[c != -1])
            for i in c:
                if celllist[i].proliferation == 1:
                    getattr(celllist[i], func)(field)
                    celllist[i].prolife(field, celllist, timedic, driver_list)
            d = field[on + r - 1 : on - r : -1, on - r].flatten()
            d = list(d[d != -1])
            for i in d:
                if celllist[i].proliferation == 1:
                    getattr(celllist[i], func)(field)
                    celllist[i].prolife(field, celllist, timedic, driver_list)

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
            nE = (self.num + self.enemynum) / Cell.K1
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
    def prepare_drug(cls, t):
        Cell.DR_STRTIME = t

    def drugged_infinity(self, t):
        if t >= Cell.DR_STRTIME and t < Cell.DR_STRTIME + Cell.DR_DURATION:
            if self.type == 1:
                dens = 1 - (self.num + self.enemynum) / Cell.KM
                self.drdeath = dens * Cell.EFFECT
            else:
                self.drdeath = 0
        if t == Cell.DR_STRTIME + Cell.DR_DURATION:
            if self.type == 1:
                self.drdeath = 0

    @classmethod
    def drtime_adjust(cls, t):
        if t == Cell.DR_STRTIME + Cell.DR_DURATION:
            Cell.DR_STRTIME += Cell.DR_INTERVAL

    @classmethod
    def drtime_list_adjust(cls, t):
        if len(Cell.drtime_list) != 0:
            if t == int(Cell.drtime_list[1]):
                del Cell.drtime_list[0:2]

    def mortal1_drug(self, field):
        if self.dead == 0:
            nE = (self.num + self.enemynum) / Cell.K1
            nE = round(nE, 3)
            if self.type == 1:
                nE += self.drdeath
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
            if self.type == 1:
                nE = (self.num + self.enemynum * Cell.WEIGHT2) / Cell.K1 + self.drdeath
                nE = round(nE, 3)
                if nE >= 1:
                    nE = 1
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

    @classmethod
    def list_adjust(cls, driver_list):
        driver_list.sort()

    @classmethod
    def make_idlist(cls, field, celllist):
        Tumor_cell.idlist = []
        refid = np.random.choice(field[field > -1], 256, replace=False)
        for i in refid:
            Tumor_cell.idlist.append(celllist[i].mutation_id)
