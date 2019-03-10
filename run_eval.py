"""
Script which runs the agents, collects results and plots graphs using
matplotlib and prints necessary values to the stdout using
"""
import sys
import matplotlib
import numpy as np
from pprint import pprint
from run_simple import SimpleAgent
from uofgsocsai import LochLomondEnv
from run_rl import QLearningAgent, run_n_trials
from run_random import RandomAgent, solve_and_display
from simple_helpers import my_best_first_graph_search

# Get the PROBLEM_ID from command line input
if len(sys.argv) == 2:
    PROBLEM_ID = int(sys.argv[1])
else:
    PROBLEM_ID = 0

"""
Collects and prints the results for the Random Agent
"""
random_agent = RandomAgent(PROBLEM_ID)
rewards, iters = random_agent.solve_and_display(10, 100)

"""
Collects and prints the results for the Simple Agent
"""
simple_agent = SimpleAgent(PROBLEM_ID)


"""
Collects and prints the results for the Q-learning Agent
"""
q_learning_agent = QLearningAgent()