import sys
import time
import math
import numpy as np
from constants import *
from search import *
from agent import Agent
from uofgsocsai import LochLomondEnv

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

    def generate_heuristics(self):
        """
        Generates the heuristic function h(n) used in the A* search algorithm,
        the heuristic being the Euclidean distance from the current node
        to the goal node. Returns a dictionary representing the value of
        h(n) for each position (i,j) in the graph
        """
        shape = self.env.desc.shape
        heuristics = np.zeros(shape, dtype=np.float64)
        goal_state = np.where(self.env.desc, b'G')
        print(goal_state)
        rows = shape[0]
        cols = shape[1]
        # Use the Euclidean distance to compute the distance to the
        # goal node
        for i in range(rows):
            for j in range(cols):
                heuristics[i,j] = math.sqrt((i - goal_state[0])**2 + (j - goal_state[1]))
        print(heuristics)
                

    def solve_and_display(self, max_episodes, max_iter_per_episode, reward_hole):
        pass

simple_agent = SimpleAgent(PROBLEM_ID, False, REWARD_HOLE)
simple_agent.generate_heuristics()