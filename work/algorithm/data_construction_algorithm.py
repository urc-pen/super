#Reverse Polish Notation
a = input().split()

def cal(ope, num1, num2):
    num1, num2 = int(num1), int(num2)
    if ope == '+':
        result = num1 + num2
    if ope == '-':
        result = num2 - num1
    if ope == '*':
        result = num1 * num2
    return result

stack = []

for i in a:
    if i.isdigit() == True:
        stack.append(i)
    else:
        stack.append(cal(i, stack.pop(), stack.pop()))

print(stack.pop())
