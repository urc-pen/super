import numpy as np
import random
import math
import fractions
import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
import matplotlib.animation as animation

interval = 0

num1 = [99771,98561,97071,95350,93602,91856,89839,87810,85629,83095,80249,77255,74099,70433,66844,63141,59339,55173,50873,46709,42464,38252,34174,30262,26459,22835,19481,16451,13764,11384,9205,7455,5972,4730,3788,3040,2389,1880,1482,1151,879,674,516,411,314,242,199,147,107,86,63,53,39,32,24,20,16,11,7,6,4,3,3,4,4,4,3,2,2,2,2,2,2,2,2,2,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]

num2 = [9,9,9,8,9,10,9,11,10,9,8,8,7,7,8,10,10,10,11,10,10,10,9,11,13,15,16,16,15,15,15,15,19,21,22,24,27,28,28,28,30,32,33,37,40,45,47,53,54,53,54,56,63,65,70,73,80,86,91,96,99,103,115,125,133,137,148,159,170,177,183,196,211,226,243,257,271,285,298,321,338,345,371,398,426,447,468,483,505,537,557,583,609,632,665,707,739,773,803,835,869,910,935,963,999,1048,1092,1157,1193,1250,1301,1360,1414,1457,1492,1551,1620,1667,1726,1796,1848,1912,1986,2050,2117,2193,2269,2368,2458,2567,2632,2680,2783,2848,2919,3010,3112,3212,3319,3407,3552,3664,3761,3871,3973,4089,4213,4318,4435,4570,4765,4919,5057,5171,5315,5457,5603,5769,5905,6056,6256,6439,6612,6815,7022,7242,7381,7582,7733,7917,8159,8384,8700,8888,9114,9344,9543,9808,10016,10254,10503,10780,11066,11366,11695,12054,12332,12566,12859,13222,13582,13894,14269,14643,15034,15408,15746,16127,16552,16979,17357,17885,18338,18749,19206,19641,20054,20522,21028,21500,22145,22690,23240,23635,24123,24713,25328,25911,26528,27080,27679,28285,28973,29527,30171,30851,31471,32174,32922,33650,34395,35202,35939,36740,37411,38160,38973,39762,40728,41533,42489,43414,44404,45388,46382,47400,48365,49437,50565,51596,52792,54035,55267,56372,57435,58604,59895,61141,62433,63751,65056,66471,68021,69517,70906,72332,73931,75440,76983,78590,80321,81911,83566,85221,86822,88594,90384,92444,94386,96362,98354,100261,102257,104341,106397,108418,110532]

t1list = range(0, len(num1), 1)
t2list = range(0, len(num2), 1)

fig = plt.figure(figsize=(10, 2))
ax1 = fig.add_subplot(1, 1, 1)

ax1.set_xlim([0, 400])
tick = range(0, 400, 50)
plt.xticks(tick)
ax1.set_yscale('log')
ax1.set_ylim([1,1000000])
tick2 = range(0, 2, 1)

ax1.set_xlabel("Time")
ax1.set_ylabel("Number of cells")

ax1.plot(t1list, num1, label="no drug-resistant", color=(0.2, 0.8, 1))
ax1.plot(t2list, num2, label="drug-resistatnt", color=(0.8, 0.1, 0.2))
time = 0
limit = max([len(num1), len(num2)])

ax1.plot([50, 50],[0, 1000000],"black", linestyle='dashed')
ax1.plot([100, 100],[0, 1000000],"black", linestyle='dashed')
ax1.plot([150, 150],[0, 1000000],"black", linestyle='dashed')
ax1.plot([200, 200],[0, 1000000],"black", linestyle='dashed')
ax1.plot([250, 250],[0, 1000000],"black", linestyle='dashed')

ax1.plot([len(num1), len(num1)],[0, 1000000],"black", linestyle='dashed')
ax1.plot([len(num2), len(num2)],[0, 1000000],"black", linestyle='dashed')

plt.axvspan(0, 10,alpha=1.0,color="#D5D5D5", label="time of dosing")

if interval == 0:
    plt.axvspan(10, limit,alpha=1.0,color="#D5D5D5")
    ax1.set_title('schedule①')

if interval == 4:
    time = 14
    ax1.set_title('schedule②')
    while time + 10 < limit:
        plt.axvspan(time, time + 10,alpha=1.0,color="#D5D5D5")
        time += 14
    if time <= limit < time + 10:
        plt.axvspan(time, limit,alpha=1.0,color="#D5D5D5")

if interval == 8:
    ax1.plot([250, 250],[0, 1000000],"black", linestyle='dashed')
    time = 18
    ax1.set_title('schedule③')
    while time + 10 < limit:
        plt.axvspan(time, time + 10,alpha=1.0,color="#D5D5D5")
        time += 18
    if time <= limit < time + 10:
        plt.axvspan(time, limit,alpha=1.0,color="#D5D5D5")

pidpng = "../result/pngstore/wayyo.png"
plt.show()
