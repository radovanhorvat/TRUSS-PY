import os

class Report:

    def __init__(self, solution, filename):
        """

        :param solution: Solver object
        """
        self.solution = solution
        self.filename = filename
        self.forces_filename = os.path.splitext(filename)[0] + '.rep'


