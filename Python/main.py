import classes
import sys

def test(filename):
    data = classes.Parser(filename)
    nodes, elements = data.get_all()
    truss = classes.Truss2D(nodes, elements)
    truss.print_info()
    input("\nPress ENTER to exit")

if __name__ == '__main__':

    filename = sys.argv[1]
    test(filename)
