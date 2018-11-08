from Cell import Cell
import numpy as np
import random
import math
import fractions
import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap

class Tumor_cell(Cell):
    driver_list = []
    timedic = {}
    dr_type = 0
    @classmethod
    def receive_value(cls,AVERAGE, DISPERSION, ENV, MTRATE, TUMORSPEED):
        super().receive_value(AVERAGE, DISPERSION, ENV)
        Cell.MTRATE = MTRATE
        Cell.TUMORSPEED = float(TUMORSPEED)


    def __init__(self, i, j):
        super().__init__(i, j)
        self.driver_mutation = 0
        self.mutation_id = 1
        self.driverflag = 0
        self.onenum = 0
        self.twonum = 0
        self.driver_type = 0

    @classmethod
    def set_first_cell(cls, field, on):
        first_cell = Tumor_cell(on, on)
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
        cell_new = Tumor_cell(ni, nj)
        cell_new.id = len(Cell.celllist)
        cell_new.mutation_id = self.mutation_id * 2 + 1
        self.mutation_id = self.mutation_id * 2
        Tumor_cell.timedic[self.mutation_id] = self.count
        Tumor_cell.timedic[cell_new.mutation_id] = self.count
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
                Tumor_cell.driver_list.append(self.mutation_id)
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
                Tumor_cell.driver_list.append(cell_new.mutation_id)
                Tumor_cell.dr_type += 1
                cell_new.driver_type = Tumor_cell.dr_type
                cell_new.driverflag = 0
        else:
            pass

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

    @classmethod
    def list_adjust(cls):
        Tumor_cell.driver_list = list(set(Tumor_cell.driver_list))
        Tumor_cell.driver_list.sort()

    @classmethod
    def countall(cls, heatmap):
        Tumor_cell.one_num = np.sum(heatmap == 1)
        Tumor_cell.two_num = np.sum(heatmap == 2)
        Tumor_cell.three_num = np.sum(heatmap == 3)

    def dead_or_alive(self, field):
        if self.type == 1:
            self.mortal(Tumor_cell.one_num, field)
        if self.type == 2:
            self.mortal(Tumor_cell.two_num, field)
        if self.type == 3:
            self.mortal(Tumor_cell.three_num, field)

    @classmethod
    def list_adjust(cls):
        Tumor_cell.driver_list.sort()

    @classmethod
    def make_idlist(cls, field):
        Tumor_cell.idlist = []
        refid = np.random.choice(field[field > -1], 256, replace=False)
        for i in refid:
            Tumor_cell.idlist.append(Cell.celllist[i].mutation_id)

    def count_around(self, r, heatmap):
        for i in range(self.i - r, self.i + r + 1):
            for j in range(self.j - r, self.j + r + 1):
                self.onenum = np.sum(heatmap[i, j] == 1)
                self.twonum = np.sum(heatmap[i, j] == 2)

    def adjust_waittime(self):
        if self.waittime == 0:
            if self.driver_mutation == 0:
                SHAPE = Cell.AVERAGE ** 2 / Cell.DISPERSION
                SCALE = Cell.DISPERSION / Cell.AVERAGE
                self.waittime = math.ceil(np.random.gamma(SHAPE, SCALE))
            if self.driver_mutation == 1:
                SHAPE = ( Cell.AVERAGE / Cell.TUMORSPEED ) ** 2 / Cell.DISPERSION
                SCALE = Cell.DISPERSION / ( Cell.AVERAGE / Cell.TUMORSPEED )
                self.waittime = math.ceil(np.random.gamma(SHAPE / 2, SCALE / 2))

    def tumor_dead_or_alive(self, field):
        if self.dead == 0:
            self.waittime_gamma()
            if self.driver_mutation == 0:
                self.dead_or_alive(field)
