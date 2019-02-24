"""
Script which defines the SimpleAgent class which uses informed search methods
(A* search) in this case to solve the LochLomondEnv problem
"""
import sys
import time
import math
import numpy as np
from constants import *
from pprint import pprint
from agent import Agent
from utils import PriorityQueue
from uofgsocsai import LochLomondEnv
from search import GraphProblem, Node, astar_search, best_first_graph_search


if len(sys.argv) == 2: 
    PROBLEM_ID = int(sys.argv[1])
else: 
    PROBLEM_ID = 0


class SimpleAgent(Agent):
    """
    Class to represent a Simple Agent that uses A* search in
    order to solve the LochLomondEnv problem
    """
    def solve(self, max_episodes, max_iters_per_episode, reward_hole):
        """
        Solves the search problem using A* search, returns
        the rewards collected and the time taken in each 
        iteration
        """
        pass

    def __generate_heuristics(self):
        """
        Generates the heuristic function h(n) used in the A* search algorithm,
        the heuristic being the Euclidean distance from the current node
        to the goal node. Returns a dictionary representing the value of
        h(n) for each position (i,j) in the graph
        """
        shape = self.env.desc.shape
        heuristics = np.zeros(shape, dtype=np.float64)
        goal_state = np.where(self.env.desc == b'G')
        print(goal_state[0][0], goal_state[1][0])
        goal_x = goal_state[0][0]
        goal_y = goal_state[1][0]
        rows = shape[0]
        cols = shape[1]
        # Use the Euclidean distance to compute the distance to the
        # goal node
        for i in range(rows):
            for j in range(cols):
                heuristics[i,j] = math.sqrt((i - goal_x)**2 + (j - goal_y)**2)
        pprint(heuristics)

    def solve_and_display(self, max_episodes, max_iter_per_episode, reward_hole):
        """
        Collects, then displays the results
        """
        pass


simple_agent = SimpleAgent(PROBLEM_ID, False, REWARD_HOLE)