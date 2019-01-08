"""
Author: Andrijan Ostrun
Year:   2017.
"""
from .models import *
from nonlinear-optimizations import *
import collections

#########################################################
#   Example 2:
#   Comparing the performances of the multiple algorithms
#   in finding minimum of the function
#
#   functions: f1, f2, f3, f4
#   algorithms:
#   -> Golden cut minimization
#   -> Simplex Nelder-Mead minimization
#   -> Hooke-Jeeves minimization
#   -> Coordinate Axis search minimization
#
#########################################################

table = collections.OrderedDict()
for i in range(0, 4):
    fun = functions[i]
    x0 = fun.default_point

    results = collections.OrderedDict()
    tmp = []

    # print("Simpleks:")
    tmp.append(simplex_nelder_mead(x0, fun, print_stats=False))
    tmp.append(fun.iterations)
    results['simplex'] = tmp.copy()
    tmp.clear()
    # print("Hooke-Jeeves:")
    tmp.append(hooke_jeeves(x0, fun, print_stats=False))
    tmp.append(fun.iterations)
    results['hooke-jeeves'] = tmp.copy()
    tmp.clear()
    #print("Coordinate axis:")
    tmp.append(coordinate_axis_search(x0, fun, print_stats=False))
    tmp.append(fun.iterations)
    results['coordinate-axis'] = tmp.copy()
    tmp.clear()

    table["f{}".format(i+1)] = results.copy()
    results.clear()

for k, v in table.items():
    print(k + ":")
    for k1, v1 in v.items():
        print("\t" + k1, v1)

####################################################################
