import classes
import graphics
import sys

def test(filename):
    data = classes.Parser(filename)
    nodes, elements, loads = data.get_all()
    truss = classes.Truss2D(nodes, elements, loads)
    truss.print_info()
    print("\n=== SOLUTION")
    sol = classes.Solver(truss)
    sol.solve()
    sol.get_reactions()
    sol.get_forces_stresses()
    print("\n--- displacements")
    print(sol.u)
    print("\n--- reactions")
    print(sol.R)
    print("\n--- forces")
    print(sol.forces)
    #print(truss.dof_dict_node)

    g = graphics.Graphics(sol, data.folder)
    g.output_acad_geometry()

    input("\nPress ENTER to exit")

if __name__ == '__main__':

    filename = sys.argv[1]
    test(filename)

    # filename = r"E:\Python_Scripts\moje\DSM3\test models\truss02.tpy"
    # data = classes.Parser(filename)
    # nodes, elements, loads = data.get_all()
    # truss = classes.Truss2D(nodes, elements, loads)
    # truss.print_info()
    # print("\n=== SOLUTION")
    # sol = classes.Solver(truss)
    # sol.solve()
    # sol.get_reactions()
    # sol.get_forces_stresses()
    # print("\n--- displacements")
    # print(sol.u)
    # print("\n--- reactions")
    # print(sol.R)
    # print("\n--- forces")
    # print(sol.forces)
    # #print(truss.dof_dict_node)
    #
    # print(data.folder)
    # g = graphics.Graphics(sol, data.folder)
    # g.output_acad_geometry()
    #
    # input("\nPress ENTER to exit")
