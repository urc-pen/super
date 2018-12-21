dic = {}
list = []
id = 1
while id < 100000000000001:
    dic[id] = 10
    list.append(id)
    id *= 2

while len(list) <= 10000000:
     dic[id] = 10
     list.append(id)

for i in list:
    if i not in dic.keys():
        print(i)
