import trusspy_parser
import trusspy_structure
import trusspy_solver
import trusspy_graphics
import sys

def test(filename):
    data = trusspy_parser.Parser(filename)
    nodes, elements, loads = data.get_all()
    truss = trusspy_structure.Truss2D(nodes, elements, loads)
    truss.print_info_short()
    print("\nSolving ...", end=" ")
    sol = trusspy_solver.Solver(truss)
    sol.solve()
    sol.get_reactions()
    sol.get_forces_stresses()
    print("DONE")
    print("Generating output ...", end=" ")
    g = trusspy_graphics.Graphics(sol, data.filename)
    g.output_geometry()
    g.output_displacements()
    g.output_forces()
    g.output_stresses()
    g.output_reactions()
    print("DONE")

    input("\nPress ENTER to exit")

if __name__ == '__main__':

    filename = sys.argv[1]
    test(filename)

    # filename = r'E:\Python_Scripts\moje\DSM3\test models\test02\Drawing1.tpy'
    # data = trusspy_parser.Parser(filename)
    # nodes, elements, loads = data.get_all()
    # truss = trusspy_structure.Truss2D(nodes, elements, loads)
    # truss.print_info_short()
    # print("\nSolving ...", end=" ")
    # sol = trusspy_solver.Solver(truss)
    # sol.solve()
    # sol.get_reactions()
    # sol.get_forces_stresses()
    # print("DONE")
    # print("Generating output ...", end=" ")
    # g = trusspy_graphics.Graphics(sol, data.filename)
    # g.output_geometry()
    # g.output_displacements()
    # g.output_forces()
    # g.output_stresses()
    # g.output_reactions()
    # print("DONE")
    #
    # input("\nPress ENTER to exit")