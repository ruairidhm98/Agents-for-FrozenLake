"""
Script which runs the agents, collects results and plots graphs using
matplotlib and prints necessary values to the stdout using
"""
import sys
import matplotlib
import numpy as np
from pprint import pprint
import matplotlib.pyplot as plt
from run_simple import SimpleAgent
from uofgsocsai import LochLomondEnv
from run_rl import QLearningAgent, process_data_q
from simple_helpers import my_best_first_graph_search
from run_random import RandomAgent, solve, process_data_random
from draw_graphs import draw_mean_rewards, draw_utility_estimate_graph

# Get the PROBLEM_ID from command line input
if len(sys.argv) == 2:
    PROBLEM_ID = int(sys.argv[1])
else:
    PROBLEM_ID = 0

MAX_EPISODES = 250
MAX_ITERS_PER_EPISODE = 250
REWARD_HOLE_DEFAULT = 0.0
REWARD_HOLE_Q = -5.00

"""
Collects and prints the results for the Random Agent and draws the graphs
"""
random_agent = RandomAgent()
process_data_random(random_agent, MAX_EPISODES, MAX_ITERS_PER_EPISODE, REWARD_HOLE_DEFAULT)
"""
Collects and prints the results for the Simple Agent and draws the graphs
"""
simple_agent = SimpleAgent(PROBLEM_ID)

"""
Collects and prints the results for the Q-learning Agent and draws the graphs.
Draws:
    Mean Reward Graph vs Episode Number
    Utility Values in each State against Episode Number
"""
q_learning_agent = QLearningAgent(5, 2, alpha=None)
states = [i for i in range(64)]
process_data_q(q_learning_agent, MAX_EPISODES, MAX_ITERS_PER_EPISODE)
