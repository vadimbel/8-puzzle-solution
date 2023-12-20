import sys

from Algo import *
from Problem import Problem


def main():
    # check the command line input
    if len(sys.argv) != 10:
        print("Please provide 9 values for the puzzle")
        return

    # get the command line values, initial the starting state
    values = [int(arg) for arg in sys.argv[1:]]

    # Reshape the flat list into a 3x3 matrix and create initial_state Node
    initial_state = [values[i:i + 3] for i in range(0, 9, 3)]

    # the initial state
    initial_state = Node(initial_state)

    # create problem instance with the initial state from aboveז
    problem = Problem(initial_state)

    result = BFS(problem)
    if result is not None:
        print("BFS")
        print(problem.get_count_expand())
        print(result.display_actions())
        problem.set_count_expand(0)

    print()

    result = IDDFS(problem)
    if result is not None:
        print("IDDFS")
        print(problem.get_count_expand())
        print(result.display_actions())
        problem.set_count_expand(0)

    print()

    result = GBFS(problem)
    if result is not None:
        print("GBFS")
        print(problem.get_count_expand())
        print(result.display_actions())
        problem.set_count_expand(0)

    print()

    result = A_star_search(problem)
    if result is not None:
        print("A*")
        print(problem.get_count_expand())
        print(result.display_actions())
        problem.set_count_expand(0)


if __name__ == "__main__":
    main()
