"""
Runs the LochLomondEnv problem with a given problem ID inputted
as a command line argument
"""
import sys
from q_agent import QLearningAgent, process_data_q
from uofgsocsai import LochLomondEnv
from constants import (
    IS_STOCHASTIC_Q, REWARD_HOLE_Q, NE, RPLUS, GAMMA, ALPHA,
    MAX_EPISODES, MAX_ITERS_PER_EPISODE
)

# Read in command line argument to get the problem ID
if len(sys.argv) == 2:
    PROBLEM_ID = int(sys.argv[1])
else:
    PROBLEM_ID = 0


env = LochLomondEnv(problem_id=PROBLEM_ID,
                    is_stochastic=IS_STOCHASTIC_Q, reward_hole=REWARD_HOLE_Q)
q_learn = QLearningAgent(env, NE, RPLUS, GAMMA, ALPHA)
states = [i for i in range(64)]
process_data_q(env, q_learn, MAX_EPISODES, MAX_ITERS_PER_EPISODE, states, PROBLEM_ID, REWARD_HOLE_Q)
