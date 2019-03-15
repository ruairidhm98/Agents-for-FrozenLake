"""
Script which contains functions to process the data after the agent has
run its trials
"""
import numpy as np
from file_io_helpers import write_simple_results, write_to_file_init_states
from simple_helpers import my_astar_search


def get_s_h_g_states(env):
    """
    Helper function, returns the starting state, goal state and
    all the hole states
    """
    # Get the start and goal state to write to file
    start_index = np.where(env.desc == b'S')
    row, col = start_index[0][0], start_index[1][0]
    start = (row, col)
    end_index = np.where(env.desc == b'G')
    row, col = end_index[0][0], end_index[1][0]
    end = (row, col)

def process_data_simple(env, agent_program, problem_id, row, col):
    """
    Processes the results collected in each trial in a given
    problem ID and writes to a file statistics from the results
    """
    start = "({}, {})".format(row, col)
    goal = "({}, {})".format(row, col)
    # Write to the file the iterations it took to reach the goal state using A* search in order
    # to compare to other agents. It is not worth collecting rewards as the agent already knows
    # the problem space and doensn't need to learn anymore to solve the problem
    iterations = my_astar_search(agent_program)
    file = open("out_simple_{}.txt".format(problem_id), "w")
    write_to_file_init_states(file, problem_id, start, goal)
    write_simple_results(file, iterations)
    file.close()
