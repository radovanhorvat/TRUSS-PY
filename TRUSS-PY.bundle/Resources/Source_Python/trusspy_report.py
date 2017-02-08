import os

class Report:

    def __init__(self, solution, filename):
        """

        :param solution: Solver object
        """
        self.solution = solution
        self.filename = filename
        self.report_filename = os.path.splitext(filename)[0] + '.rep'

    def print_heading(self, heading_text):
        """

        :param heading_text: heading name to display
        :return: heading_string: string containing heading name and decoration
        """
        heading_string = ''
        text_length = len(heading_text)
        decorator = '\n' + (text_length + 4)*'#'
        middle_line = '\n# {} #'.format(heading_text)
        heading_string += decorator
        heading_string += middle_line
        heading_string += decorator
        heading_string += '\n'
        return heading_string

    def print_general_info(self):
        """

        :return: info_string: string containing general structure info
        """
        info_string = ''
        info_string += self.print_heading('GENERAL INFO')
        info_string += "\nDegrees of freedom: {}".format(self.solution.truss.NDOF)
        info_string += "\nRestrained degrees of freedom: {}".format(len(self.solution.truss.dof_list_supports))
        info_string += "\nNumber of nodes: {}".format(self.solution.truss.number_of_nodes)
        info_string += "\nNumber of elements: {}".format(self.solution.truss.number_of_elements)
        return info_string

    def print_node_info(self):
        """

        :return: info_string: string containing node info
        """
        info_string = ''
        info_string += self.print_heading('NODE INFO')
        info_string += "\nlabel  x   y   ux   uy"
        for label, node in self.solution.truss.node_dict.items():
            info_string += "\n{}   {}   {}   {}   {}".format(node.label, node.x, node.y, node.ux, node.uy)
        return info_string

    def print_element_info(self):
        """

        :return: info_string: string containing element info
        """
        info_string = ''
        info_string += self.print_heading('ELEMENT INFO')
        info_string += "\nlabel  node1   node2   L   E   A"
        for label, element in self.solution.truss.element_dict.items():
            info_string += "\n{}   {}   {}   {}   {}   {}".format(element.label, element.node_labels[0], element.node_labels[1], element.get_length(),
                                                  element.E, element.A)
        return info_string

    def generate_report(self):
        """

        :return: generates .rep file with structure info and results
        """
        pass

if __name__ == '__main__':

    pass

