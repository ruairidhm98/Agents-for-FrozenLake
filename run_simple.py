"""
Script which defines the SimpleAgent class which uses informed search methods
(A* search) in this case to solve the LochLomondEnv problem
"""
import sys
from uofgsocsai import LochLomondEnv
from helpers_simple import env2statespace, my_best_first_graph_search
from search import (
    GraphProblem, memoize, UndirectedGraph
)

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

    def __init__(self, problem_id):
        """
        Constructor to initialise the environment for the simple agent
        """
        self.env = LochLomondEnv(problem_id=problem_id,
                                 is_stochastic=False,
                                 reward_hole=0.0)
        # Use the parser to get the location in state space,
        # the set of actions in each state, the initial starting
        # state and the terminal (goal) state
        w_1, x_1, y_1, z_1 = env2statespace(self.env)
        self.state_space_locations = w_1
        self.state_space_actions = x_1
        self.state_initial_id = y_1
        self.state_goal_id = z_1
        self.map = UndirectedGraph(self.state_space_actions)
        # Create a new GraphProblem instance to specify the problem in a format
        # in which it can be sovled
        self.problem = GraphProblem('{0}'.format(self.state_initial_id),
                                    '{0}'.format(self.state_goal_id), self.map)

    def get_initial_state(self):
        """
        Returns the initial state
        """
        return self.state_initial_id

    def get_goal_state(self):
        """
        Returns the goal state
        """
        return self.get_goal_state

    def my_astar_search(self, heur=None):
        """
        Taken from Lab 3
        A* search is best-first graph search with f(n) = g(n)+h(n).
        You need to specify the h function when you call astar_search, or
        else in your Problem subclass.
        """
        print("Initial state: " + self.get_initial_state())
        print("Initial state: " + self.get_goal_state())
        # define the heuristic function
        heur = memoize(heur or self.problem.h, 'h')
        return my_best_first_graph_search(self.problem, lambda n: n.path_cost + heur(n))
