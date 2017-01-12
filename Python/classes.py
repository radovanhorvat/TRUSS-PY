import numpy as np
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

    def get_local_stiffness_matrix(self):
        k = self.get_stiffness()
        matrix = np.array([[k, 0, -k, 0],
                           [0, 0, 0, 0],
                           [-k, 0, k, 0],
                           [0, 0, 0, 0]])
        return matrix

class Truss2D:

    def __init__(self, node_dict, element_dict):
        """

        :param node_dict: dictionary - {node_label : Node2D object}
        :param element_dict: dictionary - {element_label : Element2D object}
        """
        # independent attributes
        self.node_dict = node_dict
        self.element_dict = element_dict
        # dependent attributes
        self.number_of_nodes = len(self.node_dict)
        self.number_of_elements = len(self.element_dict)

class Parser:

    def __init__(self, filename):
        """

        :param filename: file from which to parse truss data
        """
        self.filename = filename

    def get_nodes(self):
        """

        :return: dictionary - {node_label : Node2D object}
        """
        pass



if __name__ == '__main__':

    pass