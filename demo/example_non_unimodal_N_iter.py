"""
Author: Andrijan Ostrun
Year:   2017.
"""

from models import *
from nonlinear_optimizations import *
import random
import collections
from lab import timing
from tqdm import tqdm

#########################################################
#   Example 5:
#   In this example we take two dimensional non unimodal
#   function and do N iterations of the optimization algorithm
#   with the random starting point and try to find global minimum.
#   At the end we check how many iterations actually reached the
#   global minimum of the function while other iterations reached
#   one of the local minimums.
#
#   function: f5
#   -> Simplex Nelder-Mead minimization
#   -> Hooke-Jeeves minimization
#
#########################################################


@timing
def example_5():

    table = collections.OrderedDict()
    # Number of iterations
    total_iter = 100
    # Global minimum counter
    found_min = 0
    # Every value bellow min_treshold is treated as global function minimum
    min_treshold = 10e-2

    fun = functions[4]

    for i in tqdm(range(0, total_iter)):

        x0 = [random.uniform(-50, 50), random.uniform(-50, 50)]

        #x0 = [0, 0]
        results = {}
        tmp = []

        # print("Simpleks:")
        min_ans = simplex_nelder_mead(
            x0, fun, simplex_step=1, print_stats=False)
        #min_ans = hooke_jeeves(x0, fun, print_stats=False)
        tmp.append(min_ans)
        tmp.append('iterations' + str(fun.iterations))
        min_value = fun.calc(*min_ans)
        if min_value <= min_treshold:
            found_min += 1

        tmp.append(min_value)
        results['x0'] = x0
        results['simpleks'] = tmp.copy()
        tmp.clear()

        table["f{}".format(i + 1)] = results.copy()
        results.clear()

    for k, v in table.items():
        continue
        print(k + ":")
        for k1, v1 in v.items():
            print("\t" + k1, v1)

    print("Found {} / {} global minimums.".format(found_min, total_iter))


example_5()


####################################################################
