
class Graphics:

    def __init__(self, solution, folder):
        """

        :param solution: Solver object
        """
        self.solution = solution
        self.folder = folder
        self.geometry_filename = self.folder + '\geom.scr'

    def autolisp_parse(self, command, *args):
        """
            Returns string with autolisp command,
            followed by arguments and pair of
            quotes representing carriage return.
            command must be entered as string, args
            are numbers or tuples.
            Example: autolisp_parse("line", 0, (1,2,3))
            returns: '(COMMAND "line" "0" "1,2,3" "")'
        """
        arguments = list(args)
        com = '(COMMAND-S ' + '"' + str(command) + '" '
        for item in arguments:
            if type(item) == type(tuple()):
                com += '"'
                for num in item:
                    com += str(num) + ','
                x = list(com)
                del (x[-1])
                com = "".join(x)
                com += '" '
            else:
                com += '"' + str(item) + '" '
        # com += '"")'
        return com

    def output_acad_geometry(self):
        """

        :param filename: name of .scr file to be created
        :return:
        """
        f = open(self.geometry_filename, "w")
        # drawing elements
        f.write(';**************************\n')
        f.write(';NODES, ELEMENTS AND LABELS\n')
        f.write(';**************************\n')
        f.write('COMMANDLINEHIDE\n')
        f.write('(SETQ OLDMODE (GETVAR "OSMODE"))\n')
        f.write('(SETVAR "OSMODE" 0)\n')
        f.write('(SETVAR (CMDECHO 0))\n')
        f.write('(COMMAND-S "._LAYER" "M" "TRUSSPY_output_elements" "C" "4" "" "")\n')
        f.write('(COMMAND-S "._LAYER" "M" "TRUSSPY_output_nodes" "C" "2" "" "")\n')
        added_nodes = []
        elements = self.solution.truss.element_dict
        nodes = self.solution.truss.node_dict
        f.write('(SETVAR "CLAYER" "TRUSSPY_output_elements")\n')
        for label, element in elements.items():
            node1, node2 = element.node_labels
            node1x, node1y, node1z = nodes[node1].x, nodes[node1].y, 0
            node2x, node2y, node2z = nodes[node2].x, nodes[node2].y, 0
            f.write(self.autolisp_parse('._LINE', (node1x, node1y, node1z), (node2x, node2y, node2z)) + '"")\n')
            # drawing element labels
            #f.write(autolisp_parse('TEXT', (0.5*(node1x + node2x) , 0.5*(node1y + node2y), 0.5*(node1z + node2z)), text_size, 0, str(element)) + ')\n')
        f.write('(SETVAR "OSMODE" OLDMODE)\n')
        f.write('COMMANDLINE\n')
        f.close()