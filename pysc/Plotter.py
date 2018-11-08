import math
import numpy as np
import random
import pandas as pd

class Plotter:
    @classmethod
    def receive_value(cls, POISSON):
        Plotter.POISSON = POISSON

    @classmethod
    def plot_mutation(cls, idlist, mutlist, POISSON):
        finaldict = {}
        for i in range(0, len(idlist)):
            firstdict = {}
            seconddict = {}
            thirddict = {}
            varno = idlist[i]
            columnno = idlist[i]
            while varno != 1:
                firstdict = {str(varno):0}
                seconddict.update(firstdict)

                varno = math.floor(varno / 2)

                if varno == 1:
                    thirddict = {"cell" + str(columnno):seconddict}
                    break

            finaldict.update(thirddict.copy())

        innerkeys = []
        innervalues = []
        for m in range(0, len(idlist)):
            key = "cell" + str(idlist[m])
            innerkey = list(finaldict[key].keys())
            innerkeys.extend(innerkey)
        innerkeys_unique = list(set(innerkeys))
        for n in range(0, len(innerkeys_unique)):
            poi = np.random.poisson(float(POISSON))
            innervalues.append(poi)

        innerdict = dict(zip(innerkeys_unique,innervalues))
        keys = list(innerdict.keys())
        for i in keys:
            if i in mutlist:
                innerdict[i] += 1

        for m in range(0, len(idlist)):
            key = "cell" + str(idlist[m])
            innerkey = list(finaldict[key].keys())
            for i in innerkey:
                finaldict[key][i] = innerdict[i]

        for m in range(0, len(idlist)):
            key = "cell" + str(idlist[m])
            innerkey = list(finaldict[key].keys())
            for i in innerkey:
                element = finaldict[key][i]
                if element == 0:
                    del finaldict[key][i]

                if element == 1:
                    if int(i) in mutlist:
                        del finaldict[key][i]
                        finaldict[key]["D" + i] = element
                    else:
                        del finaldict[key][i]
                        finaldict[key]["N" + i] = element

                if element >= 2:
                    if int(i) in mutlist:
                        del finaldict[key][i]
                        finaldict[key]["D" + i] = 1
                    else:
                        del finaldict[key][i]
                        finaldict[key]["N" + i] = 1

                    for j in range(2, element + 1):
                        finaldict[key]["N" + i + "_" + str(j)] = 1
                else:
                    pass

        df1 = pd.DataFrame(finaldict)
        df2 = df1.fillna(0)
        Plotter.df = df2.astype(int)

    @classmethod
    def write_newick(cls, idlist, celllist, timedic):
        idlist = random.sample(idlist, 50)

        new_idlist = idlist
        length = len(new_idlist)
        for i in range(0, length):
            varno = new_idlist[i]
            while varno != 1:
                varno = math.floor(varno / 2)
                new_idlist.append(varno)
        new_idlist = np.sort(list(set(new_idlist)))
        newick = "id1"
        for i in new_idlist:
            idx = "id" + str(i)
            new1 = i * 2
            new2 = i * 2 + 1
            type1 = 0
            type2 = 0
            if new1 in new_idlist and new2 in new_idlist:
                if new1 in idlist and new2 in idlist:
                    for cell in celllist:
                        if cell.mutation_id == new1:
                            type1 = cell.driver_type
                        if cell.mutation_id == new2:
                            type2 = cell.driver_type
                    newid = "(#" + str(type1) + "id" + str(new1) + ":" + str(timedic[new1]) + ",#" + str(type2) + "id" + str(new2) + ":" + str(timedic[new2]) + ")" + idx
                    newick = newick.replace(idx, newid)
                else:
                    newid = "(id" + str(new1) + ":" + str(timedic[new1]) + ",id" + str(new2) + ":" + str(timedic[new2]) + ")" + idx
                    newick = newick.replace(idx, newid)
            if new1 in new_idlist and new2 not in new_idlist:
                if new1 in idlist and new2 not in idlist:
                    for cell in celllist:
                        if cell.mutation_id == new1:
                            type1 = cell.driver_type
                    newid = "(#" + str(type1) + "id" + str(new1) + ":" + str(timedic[new1]) + ")" + idx
                    newick = newick.replace(idx, newid)
                else:
                    newid = "(id" + str(new1) + ":" + str(timedic[new1]) + ")" + idx
                    newick = newick.replace(idx, newid)
            if new1 not in new_idlist and new2 in new_idlist:
                if new1 not in idlist and new2 in idlist:
                    for cell in celllist:
                        if cell.mutation_id == new2:
                            type2 = cell.driver_type
                    newid = "(#" + str(type2) + "id" + str(new2) + ":" + str(timedic[new2]) + ")" + idx
                    newick = newick.replace(idx, newid)
                else:
                    newid = "(id" + str(new2) + ":" + str(timedic[new2]) + ")" + idx
                    newick = newick.replace(idx, newid)
            else:
                pass

        newick = "(" + newick + ":0);"
        with open("newick.txt", mode='w') as f:
            f.write(newick)
