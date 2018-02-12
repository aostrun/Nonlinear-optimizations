"""
Author: Andrijan Ostrun
Year:   2017.
"""
from models import *
from algorithms import *
import collections

#########################################################
#   Example 3:
#   This example show the problems with some algorithms
#   which can not find the real minimum of the function.
#   Function used in this example (f4) is not unimodal
#   thus function has a lots of local minimums but one
#   global minimum which only Simplex algorithm (in this example)
#   can find.
#
#   function: f4
#   -> Simplex Nelder-Mead minimization
#   -> Hooke-Jeeves minimization
#   -> Coordinate Axis search minimization
#
#########################################################

table = collections.OrderedDict()
for i in range(3, 4):
    fun = functions[i]
    x0 = [5,5]

    results = {}
    tmp = []

    #print("Simpleks:")
    tmp.append(simplex_nelder_mead(x0, fun, print_stats=False))
    tmp.append(fun.iterations)
    results['simplex'] = tmp.copy()
    tmp.clear()
    #print("Hooke-Jeeves:")
    tmp.append(hooke_jeeves(x0, fun, print_stats=False))
    tmp.append(fun.iterations)
    results['hookes'] = tmp.copy()
    tmp.clear()
    #print("Coordinate axis:")
    tmp.append(coordinate_axis_search(x0, fun, print_stats=False))
    tmp.append(fun.iterations)
    results['coordinate'] = tmp.copy()
    tmp.clear()

    table["f{}".format(i+1)] = results.copy()
    results.clear()

for k,v in table.items():
    print(k + ":")
    for k1, v1 in v.items():
        print("\t" + k1, v1)


####################################################################