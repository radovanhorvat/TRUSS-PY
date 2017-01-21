import os

class Graphics:

    def __init__(self, solution, filename):
        """

        :param solution: Solver object
        """
        self.solution = solution
        self.filename = filename
        self.forces_filename = os.path.splitext(filename)[0] + '.frc'
        self.displacements_filename = os.path.splitext(filename)[0] + '.dpl'

    def get_displacement_scale(self):
        """

        :return: scale factor for drawing displacement diagram
        """
        k = 0.025
        nodes = self.solution.truss.node_dict
        x_coordinates = [node.x for label, node in nodes.items()]
        y_coordinates = [node.y for label, node in nodes.items()]
        Lx = abs(max(x_coordinates) - min(x_coordinates))
        Ly = abs(max(y_coordinates) - min(y_coordinates))
        L = max(Lx, Ly)
        u_max = max([abs(item) for item in self.solution.u])
        if u_max == 0:
            scale = 1
        else:
            scale = round(L*k/u_max, 0)
        return scale

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
        forces = self.solution.forces
        centroid = self.solution.truss.get_centroid()
        for label, element in elements.items():
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

    def output_displacements(self):
        """

        :return: creates a file with node displacement data
                 which is read by AutoLISP command which draws displacement
                 diagram

                 file structure:

                 node1x, node1y, u1x, u1y, node2x, node2y, u2x, u2y
        """
        f = open(self.displacements_filename, "w")
        elements = self.solution.truss.element_dict
        u = -self.solution.u
        node_dofs = self.solution.truss.dof_dict_node
        centroid = self.solution.truss.get_centroid()
        for label, element in elements.items():
            node1, node2 = element.node_labels
            node1x, node1y = element.node1.get_point()
            node2x, node2y = element.node2.get_point()
            node1_dofs, node2_dofs = node_dofs[node1], node_dofs[node2]
            u1 = u.take(node1_dofs)
            u2 = u.take(node2_dofs)
            u1x, u1y = u1[0], u1[1]
            u2x, u2y = u2[0], u2[1]
            line_to_write = str(node1x) + ',' + str(node1y) + ',' + str(u1x) + ',' + str(u1y) + ',' + \
                            str(node2x) + ',' + str(node2y) + ',' + str(u2x) + ',' + str(u2y) + '\n'
            f.write(line_to_write)

        cx = centroid[0]
        cy = centroid[1]
        cz = centroid[2]
        line_to_write = str(cx) + ',' + str(cy) + ',' + str(cz) + '\n'
        f.write(line_to_write)

        scale = self.get_displacement_scale()
        line_to_write = str(scale)
        f.write(line_to_write)
        f.close()