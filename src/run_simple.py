"""
Runs the LochLomondEnv problems using the simple agent. Takes as
input a command line argument which specifies the problem ID
"""
import sys
from uofgsocsai import LochLomondEnv
from simple_agent import SimpleAgent, process_data_simple
from constants import (
    REWARD_HOLE_SIMPLE, IS_STOCHASTIC_SIMPLE
)

if len(sys.argv) == 2:
    PROBLEM_ID = int(sys.argv[1])
else:
    PROBLEM_ID = 0

env = LochLomondEnv(problem_id=PROBLEM_ID, is_stochastic=IS_STOCHASTIC_SIMPLE, reward_hole=REWARD_HOLE_SIMPLE)
simple_agent = SimpleAgent(env)
process_data_simple(env, simple_agent, PROBLEM_ID)
