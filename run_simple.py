import sys
import time
import numpy as np
from utils import *
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
