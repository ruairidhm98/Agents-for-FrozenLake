"""
Script which runs the agents, collects results and plots graphs using
matplotlib and prints necessary values to the stdout using
"""
import sys
import matplotlib
import numpy as np
from pprint import pprint
import matplotlib.pyplot as plt
from uofgsocsai import LochLomondEnv
from solve_trial import run_single_trial
from run_rl import QLearningAgent, process_data_q
from run_simple import SimpleAgent, process_data_simple
from run_random import RandomAgent, process_data_random
from draw_graphs import draw_mean_rewards, draw_utility_estimate_graph


# Reads command line argument and stores # in PROBLEM_ID,
# to specify the problem if this hasnt been provided, then
# just set a deafult
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
Draws:
    Mean Reward per Episode vs Episode Number
"""
env = LochLomondEnv(problem_id=PROBLEM_ID, is_stochastic=True, reward_hole=REWARD_HOLE_DEFAULT)
random_agent = RandomAgent()
process_data_random(env, random_agent, MAX_EPISODES, MAX_ITERS_PER_EPISODE, REWARD_HOLE_DEFAULT, PROBLEM_ID)
del env
"""
Collects and prints the results for the Simple Agent and draws the graphs
"""
env = LochLomondEnv(problem_id=PROBLEM_ID, is_stochastic=False, reward_hole=REWARD_HOLE_DEFAULT)
simple_agent = SimpleAgent(env)
process_data_simple(env, simple_agent, PROBLEM_ID)
del env
"""
Collects and prints the results for the Q-learning Agent and draws the graphs.
Draws:
    Mean Reward per Episode vs Episode Number
    Utility Values in each State against Episode Number
"""
states = [i for i in range(64)]
env = LochLomondEnv(problem_id=PROBLEM_ID, is_stochastic=True, reward_hole=REWARD_HOLE_Q)
q_learning_agent = QLearningAgent(env, 10, 5, alpha=lambda n: 1./(1+n))
process_data_q(env, q_learning_agent, MAX_EPISODES, MAX_ITERS_PER_EPISODE, states, PROBLEM_ID)
del env
