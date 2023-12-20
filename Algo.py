
from Node import Node
from Problem import Problem
from collections import deque

"""
This file contains implementation of BFS, IDDFS, GBFS and A*
"""


def BFS(problem: Problem):
    """
    Implementation of 'BFS' search that will be activated in 'Tiles.py' file.
    :param problem: Object of class 'Problem'.
    :return: Object of class 'Node' represents the state was searched.
    """
    # get initial state from 'Problem' class
    initial_state = problem.get_initial_state()
    # create frontier queue that will store all state needs to be explored
    frontier_queue = deque()
    # insert initial state into frontier
    frontier_queue.append(initial_state)
    # create explored set (states that already been checked)
    explored = []

    # run loop until find the solution
    while frontier_queue:
        if not frontier_queue:
            return None

        # pop the next state to be checked
        curr_state = frontier_queue.popleft()

        # check if current state is a goal state
        if problem.check_goal(curr_state):
            return curr_state

        # add checked state to explored
        explored.append(curr_state.get_state())

        # explore current state (expand)
        successors = problem.actions(curr_state)

        # run loop on all successors and add all states that was not checked to frontier
        for s in successors:
            s_matrix = s.get_state()
            if s_matrix not in explored:
                frontier_queue.append(s)

    return None


def IDDFS(problem: Problem):
    """
    Implementation of IDDFS, will be activated in 'Tiles.py' file.
    :param problem: Object of class 'Problem'.
    :return: Object of class 'Node' represents the state was searched.
    """
    # run loop until depth=30, activate DFS search each time with depth=i
    for i in range(0, 30):
        result = DFS(problem, i)

        if isinstance(result, Node):
            return result


def DFS(problem: Problem, limit: int):
    """
    Implementation of DFS, will be used in IDDFS.
    :param problem: Object of class 'Problem'.
    :param limit: integer represent a limit=max depth.
    :return: value returned from 'RecursiveDLS'.
    """
    # the initial state
    initial_state = problem.get_initial_state()
    # create data structure that will store visited states
    explored = []

    return RecursiveDLS(initial_state, problem, limit, explored)


def RecursiveDLS(curr_state: Node, problem: Problem, limit: int, explored: list):
    # flag indicates if depth=limit when performed search
    cutoff_occurred = False

    # data structure to store all states that was already checked
    explored.append(curr_state.get_state())

    # if current state depth = limit -> we reached limit depth without finding the solution
    if curr_state.get_depth() == limit:
        return 'cutoff'

    # check if current state is the goal state
    elif problem.check_goal(curr_state):
        return curr_state

    # get all sons states of current state (expand)
    successors = problem.actions(curr_state)

    # check every son state
    for s in successors:
        # if state was checked, do not check this state
        if s.get_state() in explored:
            continue
        # else - check the state
        result = RecursiveDLS(s, problem, limit, explored)

        # we reached limit depth without finding the solution
        if result == 'cutoff':
            cutoff_occurred = True
        else:
            if result != 'failure' and result != 'skip':
                return result
    # we reached limit depth without finding the solution -> return cutoff
    if cutoff_occurred:
        return 'cutoff'
    # else return failure
    return 'failure'


def A_star_search(problem: Problem):
    """
    Implementation of A* search, will be activated in 'Tiles.py' file.
    Heuristic value = h(n) = f(n) + g(n),
        f(n) = problem.missed_placed_rows_cols,
        g(n) = state depth
    :param problem: Object of class 'Problem'.
    :return: Object of class 'Node' represents the state was searched.
    """
    initial_state = problem.get_initial_state()

    # data structure to store all state need to be explored
    frontier = [initial_state]

    # create explored set to store explored states
    explored = [initial_state.get_state()]

    while frontier:
        # pop next Node state from frontier
        curr_state = frontier.pop(0)

        # check if state is goal state
        if problem.check_goal(curr_state):
            return curr_state

        # get all successors of current state
        successors = problem.actions(curr_state)

        # loop over successors :
        for s in successors:
            # get successors current state puzzle
            s_puzzle = s.get_state()
            # calculate successors current state priority (heuristic value)
            s_priority = problem.missed_placed_rows_cols(s)
            # set this state heuristic value
            s.set_heuristic_value(s_priority)

            # if current successor was already checked
            if s_puzzle in explored:
                # then we will search this state in frontier and check the priority of that state
                for i, state_from_frontier in enumerate(frontier):
                    # check the priority of the state stored in frontier, and replace data if priority is greater
                    if s_puzzle == state_from_frontier.get_state():
                        if s_priority + s.get_depth() < state_from_frontier.get_heuristic_value() + state_from_frontier.get_depth():
                            frontier[i] = s
                            # we reached puzzle configuration from different way, so we will update the depth
                            s.set_depth(curr_state.get_depth() + 1)
                            break
            # current successor not in frontier, append to 'explored' and 'frontier'
            else:
                explored.append(s_puzzle)
                frontier.append(s)

        # sort frontier by priority, lower priority state will be first
        frontier.sort(key=lambda state: state.get_heuristic_value() + state.get_depth())

    return None


def GBFS(problem: Problem):
    """
    Implementation of GBFS search, will be used in 'Tiles.py' file.
    Heuristic value = f(n) = problem.missed_placed_rows_cols.
    :param problem: Object of class 'Problem'.
    :return: Object of class 'Node' represents the state was searched.
    """
    initial_state = problem.get_initial_state()

    # add initial state to frontier
    frontier = [initial_state]

    # create explored set to store explored states
    explored = [initial_state.get_state()]

    # while frontier is not empty:
    while frontier:
        # pop next Node state from frontier
        curr_state = frontier.pop(0)

        # check if popped item is the goal state
        if problem.check_goal(curr_state):
            return curr_state

        # get all successors of current state
        successors = problem.actions(curr_state)

        # loop over successors :
        for s in successors:
            # get current state puzzle
            s_puzzle = s.get_state()
            # get current state priority
            s_priority = problem.missed_placed_rows_cols(s)
            # set this state heuristic value
            s.set_heuristic_value(s_priority)

            # if current successor was already checked
            if s_puzzle in explored:
                # then we will search this state in frontier and check the priority of that state
                for i, state_from_frontier in enumerate(frontier):
                    # check the priority of the state stored in frontier, and replace data if priority is greater
                    if s_puzzle == state_from_frontier.get_state() and s_priority < state_from_frontier.get_heuristic_value():
                        frontier[i] = s
                        break
            # current successor not in frontier, append to 'explored and 'frontier'
            else:
                explored.append(s_puzzle)
                frontier.append(s)

        # sort frontier by priority, lower priority state will be first
        frontier.sort(key=lambda state: state.get_heuristic_value())

    return None
