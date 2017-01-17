import numpy as np
import csv
from math import hypot

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
        self.NDOF = 2*self.number_of_nodes
        self.dof_dict_node = {}
        self.dof_dict_element = {}
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

    def get_dof_labels(self):
        """

        :return: populates self.dof_dict_node, self.dof_dict_element, self.dof_list_supports
                 dicts with dof labels
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

    def get_master_stiffness_matrix(self):
        """

        :return: truss master stiffness matrix M
        """
        M =  np.zeros((self.NDOF, self.NDOF))
        for label, element in self.element_dict.items():
            m = element.get_global_stiffness_matrix()
            dofs = self.dof_dict_element[label]
            for i in range(4):
                for j in range(4):
                    M[dofs[i]][dofs[j]] += m[i][j]
        return M

class Parser:

    def __init__(self, filename):
        """

        :param filename: file from which to parse truss data
        """
        self.filename = filename
        self.node_coordinate_table = {}

    def read_block(self, block_start_name, block_end_name):
        """

        :param block_start_name: string - start name of block
        :param block_end_name: string - end name of block
        :return: list of entries between block_start_name
                 and block_end_name
        """
        block_content = []
        with open(self.filename, 'r') as csvfile:
            data = csv.reader(csvfile, delimiter=',')
            block_found = False
            for row in data:
                if row == [block_start_name]:
                    block_found = True
                    continue
                if block_found == True:
                    if row != [block_end_name]:
                        float_row = [float(x) for x in row]
                        block_content.append(float_row)
                    else:
                        break
        return block_content

    def get_nodes_elements(self):
        """

        :return: node_dict, element_dict

        node_dict - {node_label : Node2D object}
        element_dict - {element_label : Element2D object}
        """
        element_dict = {}
        node_dict = {}
        start_element_label = 1
        element_label_step = 1
        start_node_label = 1
        node_label_step = 1
        element_data = self.read_block('ELEMENTS', 'END ELEMENTS')
        node_labels = [start_node_label]
        for i, data in enumerate(element_data):
            element_label = start_element_label + i*element_label_step
            node1_x, node1_y = data[0], data[1]
            node2_x, node2_y = data[2], data[3]
            try:
                node1 = node_dict[self.node_coordinate_table[(node1_x, node1_y)]]
            except KeyError:
                node1_label = max(node_labels)
                node_labels.append(node1_label)
                self.node_coordinate_table[(node1_x, node1_y)] = node1_label
                node1 = Node2D(node1_x, node1_y, 0, 0, node1_label)
                node_dict[node1_label] = node1
            try:
                node2 = node_dict[self.node_coordinate_table[(node2_x, node2_y)]]
            except KeyError:
                node2_label = max(node_labels) + node_label_step
                node_labels.append(node2_label)
                self.node_coordinate_table[(node2_x, node2_y)] = node2_label
                node2 = Node2D(node2_x, node2_y, 0, 0, node2_label)
                node_dict[node2_label] = node2
            E = data[4]
            A = data[5]
            element = Element2D(node1, node2, E, A, element_label)
            element_dict[element_label] = element
        return node_dict, element_dict

    def get_supports(self, node_dict):
        """

        :return: updates node_dict with support info, i.e. updates
                 values of ux, uy in every node object with support
        """
        support_data = self.read_block('SUPPORTS', 'END SUPPORTS')
        for item in support_data:
            x, y = item[0], item[1]
            ux, uy = int(item[2]), int(item[3])
            node_label = self.node_coordinate_table[(x, y)]
            node_dict[node_label].ux = ux
            node_dict[node_label].uy = uy

    def get_all(self):
        nodes, elements = self.get_nodes_elements()
        self.get_supports(nodes)
        return nodes, elements

if __name__ == '__main__':

    pass
