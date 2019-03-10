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
from run_random import RandomAgent, solve
from run_rl import QLearningAgent, run_n_trials
from simple_helpers import my_best_first_graph_search

# Get the PROBLEM_ID from command line input
if len(sys.argv) == 2:
    PROBLEM_ID = int(sys.argv[1])
else:
    PROBLEM_ID = 0


def solve_and_display(agent_program, max_episodes, max_iter_per_episode, reward_hole, fn):
    """
    Solves the problem using the agent program and displays the results
    """
    rewards, iters = fn(agent_program, max_episodes, max_iter_per_episode, reward_hole)
    iters = [i for i in range(max_iter_per_episode)]
    

"""
Collects and prints the results for the Random Agent
"""
random_agent = RandomAgent()
solve_and_display(random_agent, 10, 100, 0.0, solve)
"""
Collects and prints the results for the Simple Agent
"""
simple_agent = SimpleAgent(PROBLEM_ID)


"""
Collects and prints the results for the Q-learning Agent
"""
q_learning_agent = QLearningAgent(5, 2, alpha=None)
solve_and_display(q_learning_agent, 10000, 100, -1.0, run_n_trials)
