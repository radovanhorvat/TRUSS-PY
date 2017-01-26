from trusspy_structure import Node2D, Element2D
import csv
import numpy as np

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
        start_node_label = 0
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
                node1_label = max(node_labels) + 1
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

    def get_loads(self):
        """

        :return: load_dict as {node_label: (Px, Py)}
        """
        load_dict = {}
        load_data = self.read_block('LOADS', 'END LOADS')
        for item in load_data:
            x, y = item[0], item[1]
            Px, Py = item[2], item[3]
            node_label = self.node_coordinate_table[(x, y)]
            try:
                load_dict[node_label] += np.array([Px, -Py])
            except KeyError:
                load_dict[node_label] = np.array([Px, -Py])
        return load_dict

    def get_all(self):
        nodes, elements = self.get_nodes_elements()
        self.get_supports(nodes)
        loads = self.get_loads()
        return nodes, elements, loads