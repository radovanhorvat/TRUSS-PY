from math import hypot

class Node2D:

    def __init__(self, x, y, ux=0, uy=0):
        """

        :param x: float - x coordinate
        :param y: float - y coordinate
        :param ux: binary - 0 for free, 1 for constraint
        :param uy: binary - 0 for free, 1 for constraint
        """
        self.x = x
        self.y = y
        self.ux = ux
        self.uy = uy

    def get_point(self):
        return self.x, self.y

class Element2D:

    def __init__(self, node1, node2, E, A):
        """

        :param node1: Node2D object
        :param node2: Node2D object
        :param E: float - modulus of elasticity in [kN/m^2]
        :param A: float - cross section area in [m^2]
        """
        self.node1 = node1
        self.node2 = node2
        self.E = E
        self.A = A

    def get_length(self):
        x1, y1 = self.node1.get_point()
        x2, y2 = self.node2.get_point()
        length = hypot((x2 - x1), (y2 - y1))
        return length

    def get_stiffness(self):
        L = self.get_length()
        E = self.E
        A = self.A
        stiffness = E*A/L
        return stiffness

class Truss2D:

    pass

if __name__ == '__main__':

    n1 = Node2D(1, 1)
    n2 = Node2D(3, 1)
    e1 = Element2D(n1, n2, 1, 1)
