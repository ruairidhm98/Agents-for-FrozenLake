"""
Contains constants used throughout the experiments.
"""
# Rewards for falling in a hole for the respective agent
REWARD_HOLE_RANDOM = 0.0
REWARD_HOLE_SIMPLE = 0.0
REWARD_HOLE_Q = -1.0
# The maxmimum number of episodes an agent can take and the
# maximum iteration count per episode
MAX_EPISODES = 50000
MAX_ITERS_PER_EPISODE = 1000
# Booleans indicating if the environment is stochastic or not
# for the respective agent
IS_STOCHASTIC_RANDOM = True
IS_STOCHASTIC_SIMPLE = False
IS_STOCHASTIC_Q = True
# Q-learning agent extra parameters
ALPHA = 0.8
GAMMA = 0.9
NE = 1000
RPLUS = 0.1