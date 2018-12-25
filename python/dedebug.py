import math
dic = {}
list = []
id = 100000000000000001
while id != 1:
    dic[id] = 10
    id = math.floor(id / 2)

ids = 100000000000000001
while ids != 1:
    if ids not in dic.keys():
        print(ids)
    ids = math.floor(ids / 2)
