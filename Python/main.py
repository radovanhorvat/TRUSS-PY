import classes
import graphics
import sys

def test(filename):
    data = classes.Parser(filename)
    nodes, elements, loads = data.get_all()
    truss = classes.Truss2D(nodes, elements, loads)
    truss.print_info_short()
    print("\nSolving ...", end=" ")
    sol = classes.Solver(truss)
    sol.solve()
    sol.get_reactions()
    sol.get_forces_stresses()
    print("DONE")
    print("Generating output ...", end=" ")
    g = graphics.Graphics(sol, data.filename)
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
