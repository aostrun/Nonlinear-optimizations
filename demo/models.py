from math import *


#   Functions:
#   ->f0 =  100 * (x[1] - x[0]**2)**2 + (1-x[0])**2 (Rosenbrock's "Banana" function)
#   ->f1 =  (x[0] - 4)**2 + 4 * (x[1] - 2)**2
#   ->f2 =  sum( (x[i] - i)^2 )
#   ->f3 =  abs((x[0] - x[1]) * (x[0] + x[1])) + (x[0] ** 2 + x[1] ** 2) ** 0.5
#   ->f4 =  0.5 + ( sin(sqrt(sum(x[i]^2)))^2 - 0.5 ) / (1 + 0.001 * sum(x[i]^2))^2


def fun1(*x):
    return 100 * (x[1] - x[0]**2)**2 + (1-x[0])**2


def fun2(*x):
    return (x[0] - 4)**2 + 4 * (x[1] - 2)**2


def fun3(*x):
    tmp = 0
    for i in range(0, len(x)):
        tmp += (x[i] - (i+1))**2
    return tmp


def fun4(*x):
    return abs((x[0] - x[1]) * (x[0] + x[1])) + (x[0] ** 2 + x[1] ** 2) ** 0.5


def fun5(*x):
    tmp = 0
    for i in range(0, len(x)):
        tmp += x[i]**2
    return 0.5 + ((sin(sqrt(tmp))**2 - 0.5)) / ((1 + 0.001 * tmp)**2)


def fun_gold(*x):
    return (x[0] - 4)**2


def fun_1zad(*x):
    return (x[0] - 3)**2
    # return 3


def fun_zad_3_13(*x):
    return (x[0]**2 + x[1]**2 + x[2]**2)


functions = []
functions.append(Function(fun1, [-1.9, 2], [1, 1], 0))
functions.append(Function(fun2, [0.1, 0.3], [4, 2], 0))
functions.append(Function(fun3, default_point=[0, 0, 0, 0, 0], min_value=0))
functions.append(Function(fun4, [5.1, 1.1], [0, 0], 0))
functions.append(Function(fun5))

functions.append(Function(fun_gold))
