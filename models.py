from math import *

#   Functions:
#   ->f0 =  100 * (x[1] - x[0]**2)**2 + (1-x[0])**2 (Rosenbrock's "Banana" function)
#   ->f1 =  (x[0] - 4)**2 + 4 * (x[1] - 2)**2
#   ->f2 =  sum( (x[i] - i)^2 )
#   ->f3 =  abs((x[0] - x[1]) * (x[0] + x[1])) + (x[0] ** 2 + x[1] ** 2) ** 0.5
#   ->f4 =  0.5 + ( sin(sqrt(sum(x[i]^2)))^2 - 0.5 ) / (1 + 0.001 * sum(x[i]^2))^2

class function:

    def __init__(self, exp, default_point=[0,0], point_min=[0], min_value=0):
        """
        :param exp: expression that defines the function
        :param default_point: default starting point for the function
        :param point_min: point where the function reaches minimum value
        :param min_value: minimum value of the function
        """
        self.iterations = 0
        self.expression = exp
        self.default_point = default_point
        self.point_min = point_min
        self.min_value = min_value

    def reset_iterations(self):
        self.iterations = 0

    def calc(self, *args):
        """
        Calculates the value of the function for the given point.
        Function also track the number of calls.
        :param args: point
        :return: value of the function at the provided point
        """
        self.iterations+=1
        return self.expression(*args)


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
    #return 3

def fun_zad_3_13(*x):
    return (x[0]**2 + x[1]**2 + x[2]**2)

functions = []
functions.append(function(fun1, [-1.9, 2], [1,1], 0))
functions.append(function(fun2, [0.1, 0.3], [4,2], 0))
functions.append(function(fun3, default_point=[0,0,0,0,0], min_value=0))
functions.append(function(fun4,[5.1, 1.1], [0,0], 0))
functions.append(function(fun5))

functions.append(function(fun_gold))
