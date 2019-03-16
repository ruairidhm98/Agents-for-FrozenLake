"""
Script which defines the SimpleAgent class which uses informed search methods
(A* search) in this case to solve the LochLomondEnv problem
"""
import sys
import numpy as np
from uofgsocsai import LochLomondEnv
from search import GraphProblem, memoize, UndirectedGraph
from file_io_helpers import write_simple_results, write_to_file_init_states
from simple_helpers import env2statespace, my_best_first_graph_search, my_astar_search

# Read in problem ID ad command line argument, and provide default if
# one wasnt provided
if len(sys.argv) == 2:
    PROBLEM_ID = int(sys.argv[1])
else:
    PROBLEM_ID = 0


class SimpleAgent:
    """
    Class to represent a Simple Agent that uses A* search in
    order to solve the LochLomondEnv problem
    """

    def __init__(self, env):
        """
        Constructor to initialise the environment for the simple agent
        """
        # Use the parser to get the location in state space,
        # the set of actions in each state, the initial starting
        # state and the terminal (goal) state
        w_1, x_1, y_1, z_1 = env2statespace(env)
        self.state_space_locations = w_1
        self.state_space_actions = x_1
        self.state_initial_id = y_1
        self.state_goal_id = z_1
        self.map = UndirectedGraph(self.state_space_actions)
        # Create a new GraphProblem instance to specify the problem in a format
        # in which it can be sovled
        self.problem = GraphProblem('{0}'.format(self.state_initial_id),
                                    '{0}'.format(self.state_goal_id), self.map)


def process_data_simple(env, agent_program, problem_id):
    """
    Processes the results collected in each trial in a given
    problem ID and writes to a file statistics from the results
    """
    # Get the start and goal state to write to file
    start_index = np.where(env.desc == b'S')
    row, col = start_index[0][0], start_index[1][0]
    start = "({}, {})".format(row, col)
    end_index = np.where(env.desc == b'G')
    row, col = end_index[0][0], end_index[1][0]
    goal = "({}, {})".format(row, col)
    # Write to the file the iterations it took to reach the goal state using A* search in order
    # to compare to other agents. It is not worth collecting rewards as the agent already knows 
    # the problem space and doensn't need to learn anymore to solve the problem
    iterations = my_astar_search(agent_program)
    file = open("out_simple_{}.txt".format(problem_id), "w")
    write_to_file_init_states(file, problem_id, start, goal)
    write_simple_results(file, iterations)
    file.close()
