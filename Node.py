
class Node:
    """
    Class Node, represent the states.
    """
    def __init__(self, state: list, parent=None, action=None):
        """
        Create state node, each node will have attributes:
        :param state: puzzle configuration.
        :param parent: Object of class 'Node', the previous configuration that we reach to this configuration from.
        :param action: Value of the tile was moved in parent configuration.
        """
        self.state = state
        self.parent = parent
        self.action = action
        self.heuristic_value = 0
        self.depth = 0
        if parent:
            self.depth = parent.depth + 1

    def get_state(self):
        return self.state

    def get_depth(self):
        return self.depth

    def set_depth(self, new_value):
        self.depth = new_value

    def get_heuristic_value(self):
        return self.heuristic_value

    def set_heuristic_value(self, new_value):
        self.heuristic_value = new_value

    def display_actions(self):
        """
        Method that will display all tiles value that was moved to reach to goal state.
        :return: A list contains all numbers of tiles.
        """
        actions_list = []

        # Start from the current node and move upwards to the root
        current = self
        while current.parent is not None:
            if current.action is not None:
                actions_list.append(current.action)
            current = current.parent

        # Reverse the list to display actions from start to goal
        actions_list.reverse()

        return actions_list
