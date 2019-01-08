import math
import copy
from .function import Function

EPSILON = 10e-6
ITER_LIMIT = 50000

###########################GOLDEN SECTION SEARCH START#######################


def golden_section_search(var1, func, point=True, e=EPSILON, idx=0, print_stats=False):
    """
    Golden section search algorithm
    :param var1: Can be list with two elements representing the interval or can be single number from which we find unimodal interval.
    :param func: Function that is subjected to the optimization
    :param point: If set to True then var1 is a single number representing point otherwise var1 is interval (list(2))
    :param e: Error epsilon
    :param idx: Dimension that this algorithm is applied to, for example if you provide two dimensional function
                you need to provide in which dimension you want to optimize because this algorithm works only in one dimension.
                Default is 0, if the function is one dimensional leave default value 0.
    :param print_stats: If set to True function will print steps to the console.
    :return: Interval in which function reaches its minimum.
    """

    # func.reset_iterations()

    if not isinstance(func, Function):
        raise ValueError("func parameter has to be of type Function")

    if point == False and isinstance(var1, list) and len(var1) == 2:
        [a, b] = var1
    elif point == True and isinstance(var1, list):
        [a, b] = _unimodal_interval(var1, idx, func)

    k = 0.5 * (math.sqrt(5) - 1)

    c = copy.deepcopy(b)
    d = copy.deepcopy(a)

    c[idx] = b[idx] - k * (b[idx] - a[idx])
    d[idx] = a[idx] + k * (b[idx] - a[idx])
    fc = func.calc(*c)
    fd = func.calc(*d)

    while (b[idx] - a[idx]) > e:
        if fc < fd:
            b[idx] = d[idx]
            d[idx] = c[idx]
            c[idx] = b[idx] - k * (b[idx] - a[idx])
            fd = fc
            fc = func.calc(*c)
        else:
            a[idx] = c[idx]
            c[idx] = d[idx]
            d[idx] = a[idx] + k * (b[idx] - a[idx])
            fc = fd
            fd = func.calc(*d)
        if print_stats == True:
            print("a: {0} c: {1} d: {2} b: {3} fc: {4} fd: {5}".format(
                a[idx], c[idx], d[idx], b[idx], fc, fd))

    return [a, b]
    # return (a + b) / 2


def _unimodal_interval(point, idx, func, h=1):

    if not isinstance(func, Function):
        raise ValueError("func parameter has to be of type Function")

    # if func.dim != 1:
    #   raise AttributeError("Unimodal search doesn't apply to multi dimension functions!")

    l = copy.deepcopy(point)
    l[idx] -= h
    r = copy.deepcopy(point)
    r[idx] += h
    m = copy.deepcopy(point)
    step = 1

    fm = func.calc(*point)
    fl = func.calc(*l)
    fr = func.calc(*r)

    if fm < fr and fm < fl:
        return [l, r]
    elif fm > fr:
        while True:
            l = m
            m = copy.deepcopy(r)
            fm = fr
            step *= 2
            r[idx] = point[idx] + h * step
            fr = func.calc(*r)
            if fm <= fr:
                break
    else:
        while True:
            r = m
            m = copy.deepcopy(l)
            fm = fl
            step *= 2
            l[idx] = point[idx] - h * step
            fl = func.calc(*l)
            if fm <= fl:
                break

    return [l, r]

###########################GOLDEN SECTION SEARCH END#########################


###########################SIMPLEX NELDER-MEAD START#######################

def simplex_nelder_mead(point, func, alpha=1, beta=0.5, gama=2, simplex_step=1, e=EPSILON, iteration_limit=ITER_LIMIT, print_stats=False):
    """
    Simplex Nelder-Mead optimization algorithm
    :param point: Starting point from which algorithm starts
    :param func: Function that is subjected to the optimization
    :param alpha: Alpha parameter of the Simplex algorithm
    :param beta: Beta parameter of the Simplex algorithm
    :param gama: Gama parameter of the Simplex algorithm
    :param simplex_step: Step used for creating initial Simplex
    :param e: Error epsilon
    :param print_stats: If set to True function will print steps to the console
    :return: Point in which algorithm found the minimum of the function
    """

    if not isinstance(func, Function):
        raise ValueError("func parameter has to be of type Function")

    simplex = []
    step = simplex_step

    func.reset_iterations()

    # pocetni simpleks:
    simplex.append(point)
    n = len(point)
    tmp_a = (step / (n * math.sqrt(2)))
    a1 = tmp_a * (math.sqrt(n+1) + n - 1)
    a2 = tmp_a * (math.sqrt(n+1) - 1)

    for i in range(0, len(point)):
        tmp = []
        for j in range(0, len(point)):
            if j == i:
                tmp.append(a1)
            else:
                tmp.append(a2)
        simplex.append(tmp)

    centroid = None

    while True:
        [h, h_val] = _simplex_max_idx(simplex, func)
        [l, l_val] = _simplex_min_idx(simplex, func)

        # print(h)
        # print(l)

        # Find centroid
        centroid = _find_centroid(simplex, h)
        if print_stats == True:
            print("Centroid: " + str(centroid))

        error = _stop_condition(simplex, centroid, func)
        if error < e or func.iterations > iteration_limit:
            break

        # Redlection
        reflection_val = _expansion(centroid, simplex[h], alpha)
        if print_stats == True:
            print("Reflection: " + str(reflection_val))

        f_reflection = func.calc(*reflection_val)
        #print("functions {} {}".format(f_reflection, l_val))
        if f_reflection < l_val:
            expansion_val = _expansion(centroid, reflection_val, gama)
            if print_stats == True:
                print("Expansion: " + str(expansion_val))
            f_expansion = func.calc(*expansion_val)
            if f_expansion < h_val:
                simplex[h] = expansion_val
            else:
                simplex[h] = reflection_val
        else:
            if _check_reflection(f_reflection, simplex, h, func):
                if f_reflection < h_val:
                    simplex[h] = reflection_val
                contraction_val = _contraction(centroid, simplex[h], beta)
                if print_stats == True:
                    print("Contraction: " + str(contraction_val))
                f_contraction = func.calc(*contraction_val)
                if f_contraction < h_val:
                    simplex[h] = contraction_val
                else:
                    _shift_simplex(simplex, l)
            else:
                simplex[h] = reflection_val

    return centroid


def _stop_condition(simplex, centroid, fun):
    error = 0
    centroid_val = fun.calc(*centroid)
    for point in simplex:
        point_val = fun.calc(*point)
        # Sumiraj kvadratne razlike tocaka simpleksa i centroide
        error += (point_val - centroid_val)**2
    error *= 1/(len(simplex)-1)     # error * 1/n
    error = error**(0.5)
    return error


def _shift_simplex(simplex, l):
    for i in range(0, len(simplex)):
        if i == l:
            continue
        for j in range(0, len(simplex)-1):
            simplex[i][j] = 0.5 * (simplex[i][j] + simplex[l][j])


def _check_reflection(f_reflection, simplex, h, func):
    for i in range(0, len(simplex)):
        if i == h:
            continue
        val = func.calc(*simplex[i])
        if f_reflection <= val:
            return False
    return True


def _expansion(centroid, max, alpha):
    tmp = []
    for i in range(0, len(centroid)):
        val = (1+alpha) * centroid[i] - alpha * max[i]
        tmp.append(val)
    return tmp


def _expansion(centroid, reflection, gama):
    tmp = []
    for i in range(0, len(centroid)):
        val = (1-gama) * centroid[i] + gama * reflection[i]
        tmp.append(val)
    return tmp


def _contraction(centroid, max, beta):
    tmp = []
    for i in range(0, len(centroid)):
        val = (1-beta) * centroid[i] + beta * max[i]
        tmp.append(val)
    return tmp


def _find_centroid(simplex, max_idx):
    tmp = []
    for i in range(0, len(simplex)-1):
        tmp.append(0)

    for i in range(0, len(simplex)):
        if i == max_idx:
            continue
        for j in range(0, len(simplex[i])):
            tmp[j] += simplex[i][j]

    for i in range(0, len(tmp)):
        tmp[i] /= (len(simplex) - 1)

    return tmp


def _simplex_min_idx(simplex, func):
    min = func.calc(*simplex[0])
    min_idx = 0
    for i in range(1, len(simplex)):
        f = func.calc(*simplex[i])
        if f < min:
            min = f
            min_idx = i
    return [min_idx, min]


def _simplex_max_idx(simplex, func):
    max = func.calc(*simplex[0])
    max_idx = 0
    for i in range(1, len(simplex)):
        f = func.calc(*simplex[i])
        if f > max:
            max = f
            max_idx = i
    return [max_idx, max]

###########################SIMPLEX NELDER-MEAD END###########################


###########################HOOKE-JEEVES START################################

def hooke_jeeves(point, func, dx=0.5, e=EPSILON, print_stats=False):
    """
    Hooke-Jeeves optimization algorithm
    :param point: Starting point from which algorithm starts
    :param func: Function that is subjected to the optimization
    :param dx: Initial step that algorithm uses to move points, every iteration step is divided by 2
    :param e: Error epsilon
    :param print_stats: If set to True function will print steps to the console
    :return: Point in which algorithm found the minimum of the function
    """

    if not isinstance(func, Function):
        raise ValueError("func parameter has to be of type Function")

    x0 = copy.deepcopy(point)
    xb = copy.deepcopy(point)
    xp = copy.deepcopy(point)
    xn = None

    func.reset_iterations()

    while True:
        if dx <= e:
            break
        xn = _hooke_jeeves_search(xp, func, dx)
        f_xn = func.calc(*xn)
        f_xb = func.calc(*xb)
        if f_xn < f_xb:
            for i in range(0, len(xn)):
                xp[i] = 2*xn[i] - xb[i]
                xb[i] = xn[i]
        else:
            dx /= 2
            xp = copy.deepcopy(xb)

        if print_stats == True:
            print("Xb: {0} Xp: {1} Xn: {2}".format(xb, xp, xn))

    return xb


def _hooke_jeeves_search(xp, func, dx):
    x = copy.deepcopy(xp)
    for i in range(0, len(xp)):
        p = func.calc(*x)
        x[i] += dx
        n = func.calc(*x)
        if n > p:
            x[i] -= 2*dx
            n = func.calc(*x)
            if n > p:
                x[i] += dx
    return x

###########################HOOKE-JEEVES END##################################


###########################COORDINATE DESCENT SEARCH START######################

def coordinate_axis_search(point, func, e=EPSILON, print_stats=False):

    if not isinstance(func, Function):
        raise ValueError("func parameter has to be of type Function")

    i = 0
    dim = len(point)

    func.reset_iterations()

    while True:
        idx = i % dim
        old = copy.deepcopy(point)
        [a, b] = golden_section_search(point, func, idx=idx, print_stats=False)
        # print(a)
        # print(b)
        point[idx] = (a[idx] + b[idx]) / 2
        i += 1

        #print("\t {}".format(point))
        if _check_error(point, old):
            break

    return point


def _check_error(point_new, point_old, e=EPSILON):
    for i in range(0, len(point_new)):
        if abs(point_new[i] - point_old[i]) > e:
            return False
    return True

###########################COORDINATE DESCENT SEARCH END#########################
