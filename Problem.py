
from Node import Node
import copy


def find_empty_spot(state: Node):
    """Find the position of the empty spot (0) in the state."""
    for i, row in enumerate(state.get_state()):
        if 0 in row:
            return i, row.index(0)
    return None


class Problem:
    """
    Problem class, represent the 8-puzzle problem.
    """
    def __init__(self, initial_state: Node):
        """
        Constructor of class Problem.
        :param initial_state: Object of class 'Node', will be created from the values that entered in command line.

        goal_state_one: First goal state.
        goal_state_two: Second goal state.
        count_expand: Amount of state were expanded.
        """
        self.initial_state = initial_state
        self.goal_state_one = Node([[1, 2, 3], [4, 5, 6], [7, 8, 0]])
        self.goal_state_two = Node([[0, 1, 2], [3, 4, 5], [6, 7, 8]])
        self.count_expand = 0


    def get_initial_state(self):
        """
        :return: Object of class 'Node'.
        """
        return self.initial_state

    def set_count_expand(self, value: int):
        """
        Set 'count_expand' attribute.
        :param value: value
        :return:
        """
        self.count_expand = value

    def get_count_expand(self):
        """
        :return: returns 'count_expand' attribute.
        """
        return self.count_expand

    def check_goal(self, state: Node):
        """
        Checks if goal state is found.
        :param state: current state to check if it is the goal state.
        :return: True/False.
        """
        state_mat = state.get_state()
        if state_mat == self.goal_state_one.get_state() or state_mat == self.goal_state_two.get_state():
            return True
        return False

    def get_goals(self):
        return [self.goal_state_one, self.goal_state_two]

    def actions(self, state: Node):
        """
        Implementation of 'expand' action.
        :param state: expand this state.
        :return: All successors of expanded state.
        """
        # find empty spot of current state
        row, col = find_empty_spot(state)

        # count expand operation
        self.set_count_expand(self.count_expand + 1)

        # list of all successors of current state
        successors = []

        if row > 0:
            # Create a deep copy of the current state
            new_state = copy.deepcopy(state.get_state())
            # Swap the empty spot with the tile above it
            new_state[row][col], new_state[row - 1][col] = new_state[row - 1][col], new_state[row][col]
            # Create a new node with the updated state
            successors.append(Node(new_state, state, new_state[row][col]))

        if col > 0:
            # Create a deep copy of the current state
            new_state = copy.deepcopy(state.get_state())
            # Swap the empty spot with the tile above it
            new_state[row][col], new_state[row][col - 1] = new_state[row][col - 1], new_state[row][col]
            # Create a new node with the updated state
            successors.append(Node(new_state, state, new_state[row][col]))

        if row < 2:
            # Create a deep copy of the current state
            new_state = copy.deepcopy(state.get_state())
            # Swap the empty spot with the tile above it
            new_state[row][col], new_state[row + 1][col] = new_state[row + 1][col], new_state[row][col]
            # Create a new node with the updated state
            successors.append(Node(new_state, state, new_state[row][col]))

        if col < 2:
            # Create a deep copy of the current state
            new_state = copy.deepcopy(state.get_state())
            # Swap the empty spot with the tile above it
            new_state[row][col], new_state[row][col + 1] = new_state[row][col + 1], new_state[row][col]
            # Create a new node with the updated state
            successors.append(Node(new_state, state, new_state[row][col]))

        return successors


    def missed_placed_rows_cols(self, curr_state: Node):
        """
        Heuristic that will be used in GBFS and A* searches.

        For each value we will check if it is in the right row and column according to the 2 goal states.
        If value is in the right row and col in one of the goal state, that means that this state must be getting us
        closer to the one of the goal state.

        :param curr_state: calculate heuristic value of this state.
        :return:
        """
        count_one = 0
        count_two = 0
        # get checked state puzzle configuration
        curr_state_puzzle = curr_state.get_state()

        # search each value in current state configuration
        for row in range(0, 3):
            for col in range(0, 3):
                puzzle_value = curr_state_puzzle[row][col]

                # skip the empty spot
                if puzzle_value == 0:
                    continue

                # for each value for current configuration :

                # find the row and col of that value in goal state 1
                correct_row_one, correct_col_one = self.find_position_in_goal_state(puzzle_value, 1)
                # if value (puzzle_value) is not in the correct row or col in goal state 1, increase 'count_one'.
                if row != correct_row_one:
                    count_one += 1
                if col != correct_col_one:
                    count_one += 1

                # do the same this for value (puzzle_value) and goal state 2
                correct_row_two, correct_col_two = self.find_position_in_goal_state(puzzle_value, 2)
                if row != correct_row_two:
                    count_two += 1
                if col != correct_col_two:
                    count_two += 1

        # return the min value from the two
        return min(count_one, count_two)


    def find_position_in_goal_state(self, puzzle_value, goal_state):
        """
        Method will be activated in 'missed_placed_rows_cols' heuristic
        :param puzzle_value: value checked in checked state.
        :param goal_state: what goal state we check.
        :return: row/col.
        """
        goal_state_puzzle = None

        if goal_state == 1:
            goal_state_puzzle = self.goal_state_one.get_state()
        else:
            goal_state_puzzle = self.goal_state_two.get_state()

        for row in range(0, 3):
            for col in range(0, 3):
                if goal_state_puzzle[row][col] == puzzle_value:
                    return row, col

        return None

