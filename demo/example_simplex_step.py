"""
Author: Andrijan Ostrun
Year:   2017.
"""

from models import *
from algorithms import *
import collections

#########################################################
#   Example 4:
#   Experimenting with the step size of the Simplex
#   algorithm. This example minimizes function 1
#   with Simplex algorithm but changes the step size
#   from 1 to 20 and we can see that algorithm is behaves
#   differently with each step size and some steps
#   are better then others.
#
#   function: f1
#   -> Simplex Nelder-Mead minimization
#
#########################################################

table = collections.OrderedDict()
for i in range(0, 1):
    fun = functions[i]
    x0 = [0.5, 0.5]

    results = collections.OrderedDict()
    for j in range(0, 20):
        tmp = []

        #print("Simpleks:")
        tmp.append(simplex_nelder_mead(x0, fun, simplex_step=j+1, print_stats=False))
        tmp.append(fun.iterations)
        results['simplex, d={}'.format(j+1)] = tmp.copy()
        tmp.clear()

    table["f{}".format(i + 1)] = results.copy()
    results.clear()

for k,v in table.items():
    print(k + ":")
    for k1, v1 in v.items():
        print("\t" + k1, v1)

####################################################################