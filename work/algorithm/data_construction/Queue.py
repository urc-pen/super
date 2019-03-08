#Queue
n = list(map(int, input().split()))
schedic = {}
que = []
time = 0

for i in range(0, n[0]):
    a = input().split()
    a[1] = int(a[1])
    schedic[a[0]] = a[1]
    que.append(a[0])

while len(que) != 0:
    id = que.pop(0)
    eachtime = schedic[id]
    if eachtime > n[1]:
        schedic[id] = eachtime - n[1]
        que.append(id)
        time += n[1]
    elif eachtime <= n[1]:
        schedic[id] = 0
        time += eachtime
        print("{0} {1}".format(id, time))
