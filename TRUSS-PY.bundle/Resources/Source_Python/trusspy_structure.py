import numpy as np
from math import hypot
import copy

class Node2D:

    def __init__(self, x, y, ux=0, uy=0, label=None):
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
        self.label = label

    def get_point(self):
        return self.x, self.y

class Element2D:

    def __init__(self, node1, node2, E, A, label=None):
        """

        :param node1: Node2D object
        :param node2: Node2D object
        :param E: float - modulus of elasticity in [kN/m^2]
        :param A: float - cross section area in [m^2]
        """
        # independent attributes
        self.node1 = node1
        self.node2 = node2
        self.E = E
        self.A = A
        self.label = label
        # dependent attributes
        self.node_labels = (self.node1.label, self.node2.label)

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

    def get_global_stiffness_matrix(self):
        k = self.get_stiffness()
        L = self.get_length()
        x1, y1 = self.node1.get_point()
        x2, y2 = self.node2.get_point()
        dx, dy = x2 - x1, y2 - y1
        c, s = dx/L, dy/L
        matrix = np.array([[k*c**2, k*s*c, -k*c**2, -k*s*c],
                           [k*s*c, k*s**2, -k*s*c, -k*s**2],
                           [-k*c**2, -k*s*c, k*c**2, k*s*c],
                           [-k*s*c, -k*s**2, k*s*c, k*s**2]])
        return matrix

    def get_transformation_matrix(self):
        L = self.get_length()
        x1, y1 = self.node1.get_point()
        x2, y2 = self.node2.get_point()
        dx, dy = x2 - x1, y2 - y1
        c, s = dx/L, dy/L
        T = np.array([[c, s, 0, 0],
                      [-s, c, 0, 0],
                      [0, 0, c, s],
                      [0, 0, -s, c]])
        return T

class Truss2D:

    def __init__(self, node_dict, element_dict, load_dict):
        """

        :param node_dict: dictionary - {node_label : Node2D object}
        :param element_dict: dictionary - {element_label : Element2D object}
        """
        # independent attributes
        self.node_dict = node_dict
        self.element_dict = element_dict
        self.load_dict = load_dict
        # dependent attributes
        self.number_of_nodes = len(self.node_dict)
        self.number_of_elements = len(self.element_dict)
        self.NDOF = 2*self.number_of_nodes
        self.dof_dict_node = {}
        self.dof_dict_element = {}
        self.dof_dict_loads = {}
        self.dof_list_supports = []
        # function calls upon instantiation
        self.get_dof_labels()

    def print_info(self):
        print("=== STRUCTURE INFO")
        print("\n--- GENERAL")
        print("DOF: {}".format(self.NDOF))
        print("# nodes: {}".format(self.number_of_nodes))
        print("# elements: {}".format(self.number_of_elements))
        print("\n--- NODES")
        print("label  x   y   ux   uy")
        for label, node in self.node_dict.items():
            print("{}   {}   {}   {}   {}".format(node.label, node.x, node.y, node.ux, node.uy))
        print("\n--- ELEMENTS")
        print("label  nodes  L   E   A")
        for label, element in self.element_dict.items():
            print("{}   {}   {}   {}   {}".format(element.label, element.node_labels, element.get_length(),
                                                  element.E, element.A))
        print("\n--- LOADS")
        print("node  Px   Py")
        for node_label, load in self.load_dict.items():
            print("{}   {}   {}".format(node_label, load[0], load[1]))

    def print_info_short(self):
        print("=== STRUCTURE INFO")
        print("\n# DOF: {}".format(self.NDOF))
        print("# nodes: {}".format(self.number_of_nodes))
        print("# elements: {}".format(self.number_of_elements))
        print("# supports: {}".format(len(self.dof_list_supports)))
        print("# loads: {}".format(len(self.dof_dict_loads)))

    def get_dof_labels(self):
        """

        :return: populates self.dof_dict_node, self.dof_dict_element, self.dof_list_supports
                 and self.dof_dict_loads dicts with dof labels
        """
        i = 0
        for node_label, node in self.node_dict.items():
            dof_x, dof_y = 2*i, 2*i + 1
            self.dof_dict_node[node_label] = (dof_x, dof_y)
            if node.ux == 1:
                self.dof_list_supports.append(dof_x)
            if node.uy == 1:
                self.dof_list_supports.append(dof_y)
            i += 1
        for element_label, element in self.element_dict.items():
            node1_label = element.node_labels[0]
            node2_label = element.node_labels[1]
            self.dof_dict_element[element_label] = self.dof_dict_node[node1_label] + self.dof_dict_node[node2_label]
        for node_label, load in self.load_dict.items():
            Px, Py = load[0], load[1]
            dof_x, dof_y = self.dof_dict_node[node_label]
            if Px != 0:
                self.dof_dict_loads[dof_x] = Px
            if Py != 0:
                self.dof_dict_loads[dof_y] = Py

    def get_master_stiffness_matrix(self):
        """

        :return: truss master stiffness matrix M modified for
                 boundary conditions
        """
        M =  np.zeros((self.NDOF, self.NDOF))
        for label, element in self.element_dict.items():
            m = element.get_global_stiffness_matrix()
            dofs = self.dof_dict_element[label]
            for i in range(4):
                for j in range(4):
                    M[dofs[i]][dofs[j]] += m[i][j]
        return M

    def modify_master_stiffness_matrix(self, M):
        """

        :param M: master stiffnes matrix
        :return: modified master stiffness matrix to account
                 for boundary conditions
        """
        M_mod = copy.copy(M)
        for dof in self.dof_list_supports:
            M_mod[dof, :] = 0
            M_mod[:, dof] = 0
        for i in range(self.NDOF):
            if M_mod[i][i] == 0:
                M_mod[i][i] = 1
        return M_mod

    def get_load_vector(self):
        """

        :return: global load vector modified for
                 boundary conditions
        """
        F = np.zeros(self.NDOF)
        for dof, load in self.dof_dict_loads.items():
            F[dof] += load
        return F

    def modify_load_vector(self, F):
        """

        :param F: global load vector
        :return: modified global load vector to account
                 for boundary conditions
        """
        F_mod = copy.copy(F)
        for dof in self.dof_list_supports:
            F_mod[dof] = 0
        return F_mod

    def get_centroid(self):
        """

        :return: centroid of nodes as tuple (xc, yc, 0)
        """
        xc, yc = 0, 0
        for label, node in self.node_dict.items():
            x, y = node.get_point()
            xc += x
            yc += y
        xc = xc/self.number_of_nodes
        yc = yc/self.number_of_nodes
        return xc, yc, 0