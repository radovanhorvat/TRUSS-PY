import numpy as np

class Solver:

    def __init__(self, truss):
        """

        :param truss: Truss2D object
        """
        # initialization of vectors and matrices
        self.truss = truss
        self.M = self.truss.get_master_stiffness_matrix()
        self.M_mod = self.truss.modify_master_stiffness_matrix(self.M)
        self.F = self.truss.get_load_vector()
        self.F_mod = self.truss.modify_load_vector(self.F)
        # solution data
        self.u = None
        self.R = None
        self.forces = {}
        self.stresses = {}

    def solve(self):
        """

        :return: displacement vector u
        """
        self.u = np.linalg.solve(self.M_mod, self.F_mod)

    def get_reactions(self):
        """

        :return: reaction vector R
        """
        self.R = np.dot(self.M, self.u) - self.F

    def get_forces_stresses(self):
        """

        :return:
        """
        for label, element in self.truss.element_dict.items():
            T = element.get_transformation_matrix()
            dofs = self.truss.dof_dict_element[label]
            u_global = np.take(self.u, dofs)
            u_local = np.dot(T, u_global)
            du = u_local[2] - u_local[0]
            k = element.get_stiffness()
            F = k*du
            s = F/element.A
            self.forces[label] = F
            self.stresses[label] = s