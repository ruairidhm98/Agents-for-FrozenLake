"""
Runs the LochLomondEnv problem using the random agent. Takes as input
a command line argument which specifies the problem ID.
"""
import sys
from uofgsocsai import LochLomondEnv
from random_agent import RandomAgent, process_data_random
from constants import (
    REWARD_HOLE_RANDOM, MAX_EPISODES, MAX_ITERS_PER_EPISODE,
    IS_STOCHASTIC_RANDOM
)

if len(sys.argv) == 2:
    PROBLEM_ID = int(sys.argv[1])
else:
    PROBLEM_ID = 0

env = LochLomondEnv(problem_id=PROBLEM_ID, is_stochastic=IS_STOCHASTIC_RANDOM, reward_hole=REWARD_HOLE_RANDOM)
rand_agent = RandomAgent(env)
process_data_random(env, rand_agent, MAX_EPISODES, MAX_ITERS_PER_EPISODE, REWARD_HOLE_RANDOM, PROBLEM_ID)
