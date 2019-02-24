"""
Script which defines the SimpleAgent class which uses informed search methods
(A* search) in this case to solve the LochLomondEnv problem
"""
import sys
import time
from math import sqrt
import numpy as np
from constants import MAX_EPISODES, MAX_ITERS_PER_EPISODE, REWARD_HOLE
from agent import Agent
from simple_helpers import generate_heuristics
from uofgsocsai import LochLomondEnv

# Read in problem ID ad command line argument, and provide default if
# one wasnt provided
if len(sys.argv) == 2:
    PROBLEM_ID = int(sys.argv[1])
else:
    PROBLEM_ID = 0


class Problem:
    """
    Class which represents the problem the agent is trying to save
    """
    def __init__(self, initial, goal, graph):
        """
        Constructor, which initialses the initial state, the goal state,
        the graph being searched and heuristics that will inform the agent
        of the problem in advance
        """
        self.initial = initial
        self.goal = goal
        self.graph = graph
        self.heuristics = generate_heuristics(self.graph)

    def is_goal_state(self, state):
        """
        Returns true if and only if the state parameter
        is the goal state
        """
        return self.goal == state


class SimpleAgent(Agent):
    """
    Class to represent a Simple Agent that uses A* search in
    order to solve the LochLomondEnv problem
    """
    def __solve(self, max_episodes, max_iters_per_episode, reward_hole):
        """
        Solves the search problem using A* search, returns
        the rewards collected and the time taken in each
        iteration
        """
        pass

    def solve_and_display(self, max_episodes, max_iter_per_episode, reward_hole):
        """
        Collects, then displays the results
        """
        pass
