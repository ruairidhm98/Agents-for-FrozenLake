"""
Script which runs the agents, collects results and plots graphs using
maptlotlib and prints relevant tables to the stdout
"""
import sys
import numpy as np
import matplotlib
from pprint import pprint
from run_random import RandomAgent
from run_simple import SimpleAgent
from run_rl import QLearningAgent

if len(sys.argv) == 2:
    PROBLEM_ID = int(sys.argv[1])
else:
    PROBLEM_ID = 0

