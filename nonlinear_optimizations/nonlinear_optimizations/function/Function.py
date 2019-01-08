class Function:

    def __init__(self, exp, default_point=[0, 0], point_min=[0], min_value=0):
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
        self.iterations += 1
        return self.expression(*args)