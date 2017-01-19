import classes
import sys

def test(filename):
    data = classes.Parser(filename)
    nodes, elements, loads = data.get_all()
    truss = classes.Truss2D(nodes, elements, loads)
    truss.print_info()
    print("\n--- solution")
    sol = classes.Solver(truss)
    sol.solve()
    print(sol.u)
    #print(sol.R)
    #print(truss.dof_dict_node)
    input("\nPress ENTER to exit")

if __name__ == '__main__':

    filename = sys.argv[1]
    test(filename)

    # filename = r"E:\Python_Scripts\moje\DSM3\test models\truss01.tpy"
    # data = classes.Parser(filename)
    # nodes, elements, loads = data.get_all()
    # truss = classes.Truss2D(nodes, elements, loads)
    # truss.print_info()
    #
    # print("\n--- solution")
    # sol = classes.Solver(truss)
    # u = sol.solve()
    # print(u)
    # print(truss.dof_dict_node)
