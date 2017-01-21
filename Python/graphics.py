import os

class Graphics:

    def __init__(self, solution, filename):
        """

        :param solution: Solver object
        """
        self.solution = solution
        self.filename = filename
        self.forces_filename = os.path.splitext(filename)[0] + '.frc'

    def output_forces(self):
        """

        :return: creates a file with element force data
                 which is read by AutoLISP command which draws forces
                 diagram

                 file structure:

                 node1x, node1y, 0, node2x, node2y, 0, force
        """
        f = open(self.forces_filename, "w")
        elements = self.solution.truss.element_dict
        nodes = self.solution.truss.node_dict
        forces = self.solution.forces
        centroid = self.solution.truss.get_centroid()
        for label, element in elements.items():
            #node1, node2 = element.node_labels
            #node1x, node1y = nodes[node1].get_point()
            #node2x, node2y = nodes[node2].get_point()
            node1x, node1y = element.node1.get_point()
            node2x, node2y = element.node2.get_point()
            node1z = 0.0
            node2z = 0.0
            force = round(forces[label], 2)
            line_to_write = str(node1x) + ',' + str(node1y) + ',' + str(node1z) + ',' + \
                            str(node2x) + ',' + str(node2y) + ',' + str(node2z) + ',' + \
                            str(force) + '\n'
            f.write(line_to_write)
        cx = centroid[0]
        cy = centroid[1]
        cz = centroid[2]
        line_to_write = str(cx) + ',' + str(cy) + ',' + str(cz)
        f.write(line_to_write)
        f.close()
