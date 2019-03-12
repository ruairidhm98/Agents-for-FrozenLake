"""
Script which runs the agents, collects results and plots graphs using
matplotlib and prints necessary values to the stdout using. Takes as command
line argument the problem ID of the environment.
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

MAX_EPISODES = 10
MAX_ITERS_PER_EPISODE = 500
REWARD_HOLE_DEFAULT = 0.0
REWARD_HOLE_Q = -10.00

#env_random = LochLomondEnv(problem_id=PROBLEM_ID, is_stochastic=True, reward_hole=REWARD_HOLE_DEFAULT)
#env_simple = LochLomondEnv(problem_id=PROBLEM_ID, is_stochastic=False, reward_hole=REWARD_HOLE_DEFAULT)
env_qlearn = LochLomondEnv(problem_id=PROBLEM_ID, is_stochastic=True, reward_hole=REWARD_HOLE_Q)
"""print(env_random.desc)
print(env_simple.desc)
print(env_qlearn.desc)"""
"""
Collects and prints the results for the Random Agent and draws the graphs
Draws:
    Mean Reward per Episode vs Episode Number
"""
#random_agent = RandomAgent()
#process_data_random(env_random, random_agent, MAX_EPISODES, MAX_ITERS_PER_EPISODE, REWARD_HOLE_DEFAULT, PROBLEM_ID)
# print(env_random.desc)
"""
Collects and prints the results for the Simple Agent and draws the graphs
"""
#simple_agent = SimpleAgent(env_simple)
#process_data_simple(env_simple, simple_agent, PROBLEM_ID)
# print(env_simple.desc)
"""
Collects and prints the results for the Q-learning Agent and draws the graphs.
Draws:
    Mean Reward per Episode vs Episode Number
    Utility Values in each State against Episode Number
"""
states = [i for i in range(64)]
q_learning_agent = QLearningAgent(env_qlearn, 250, 15, alpha=lambda n: 3*n)
process_data_q(env_qlearn, q_learning_agent, MAX_EPISODES,
               MAX_ITERS_PER_EPISODE, states, PROBLEM_ID, REWARD_HOLE_Q)
print(q_learning_agent.Q.items())