"""
Author: Andrijan Ostrun
Year:   2017.
"""
from models import *
from nonlinear_optimizations import *
from nonlinear_optimizations.function import Function


#########################################################
#   Example 1:
#   Performing all of the implemented algorithms on the
#   minimization of function 1 and printing all the
#   steps that algorithm performed
#
#   function: f1 (Rosenbrock's "Banana" function)
#   -> Golden cut minimization
#   -> Simplex Nelder-Mead minimization
#   -> Hooke-Jeeves minimization
#   -> Coordinate Axis search minimization
#
#########################################################

fun = Function(fun_1zad)
x0 = [10]
results = {}

print("Golden cut:")
print("\nResulting point (interval): " +
      golden_section_search(x0, fun).__str__())
results['golden'] = fun.iterations
print("################################################\n")

print("Simplex:")
print("\nResulting point: " + simplex_nelder_mead(x0, fun).__str__())
results['simplex'] = fun.iterations
print("################################################\n")

print("Hooke-Jeeves:")
print("\nResulting point: " + hooke_jeeves(x0, fun).__str__())
results['H-J'] = fun.iterations
print("################################################\n")

print("Coordinate axis:")
print("\nResulting point: " + coordinate_axis_search(x0, fun).__str__())
results['Co-Ax'] = fun.iterations
print("################################################\n")

print("Cost Function calls:")
for k, v in results.items():
    print("\t {} : {}".format(k, v))

############################################################
