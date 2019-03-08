#insertion sort
n = int(input())
a = list(map(int, input().split()))

for i in range(1, n):
    v = a[i]
    j = i - 1
    while j >= 0 and a[j] > v:
        a[j+1] = a[j]
        j -= 1
    a[j+1] = v
    print(a)

#bubble sort
n = int(input())
a = list(map(int, input().split()))
flag = 1    #隣接行列が存在
while flag == 1:
    flag = 0
    for i in range(n-1, 0, -1):
        if a[i] < a[i-1]:
            a[i], a[i-1] = a[i-1], a[i]
            flag = 1
            print(a)

#selection sort
n = int(input())
a = list(map(int, input().split()))

for i in range(0, n):
    minj = i
    for j in range(i, n):
        if a[j] < a[minj]:
            minj = j
    a[i], a[minj] = a[minj], a[i]
    print(a)
