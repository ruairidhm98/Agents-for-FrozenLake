"""
Script which runs the agents, collects results and plots graphs using
matplotlib and prints necessary values to the stdout using. Takes as command
line argument the problem ID of the environment.
"""
import sys
import matplotlib
import numpy as np
import matplotlib.pyplot as plt
from uofgsocsai import LochLomondEnv
from run_rl import QLearningAgent, process_data_q
from run_simple import SimpleAgent, process_data_simple
from run_random import RandomAgent, process_data_random


# Reads command line argument and stores # in PROBLEM_ID,
# to specify the problem if this hasnt been provided, then
# just set a deafult
if len(sys.argv) == 2:
    PROBLEM_ID = int(sys.argv[1])
else:
    PROBLEM_ID = 0


ALPHA = 0.8
GAMMA = 0.9
MAX_EPISODES = 50000
MAX_ITERS_PER_EPISODE = 1000
REWARD_HOLE_DEFAULT = 0.0
REWARD_HOLE_Q = -1.00
NE = 1000
RPLUS = 0.1

env_random = LochLomondEnv(problem_id=PROBLEM_ID, is_stochastic=True, reward_hole=REWARD_HOLE_DEFAULT)
env_simple = LochLomondEnv(problem_id=PROBLEM_ID, is_stochastic=False, reward_hole=REWARD_HOLE_DEFAULT)
env_qlearn = LochLomondEnv(problem_id=PROBLEM_ID, is_stochastic=True, reward_hole=REWARD_HOLE_Q)

start_index = np.where(env_qlearn.desc == b'S')
row, col = start_index[0][0], start_index[1][0]
start = row*8 + col
end_index = np.where(env_qlearn.desc == b'G')
row, col = end_index[0][0], end_index[1][0]
goal = row*8 + col
holes = np.where(env_qlearn == b'H')
terminals = []
for i in range(len(holes[0])):
    row, col = holes[0][i], holes[1][i]
    terminals.append([row*8 + col])


def Rew(s):
    """
    Helper function, return the reward for being in state s
    """
    if s == start: return 0.0
    elif s == goal: return +1.0
    elif s in terminals: return REWARD_HOLE_Q
    else: return 0.0


def compare_utils(U1, U2, H1="U1     ", H2="U2       "):
    """
    Compares two utility tables and writes to a file the results
    """
    U_diff = dict()
    file = open("out_qagent_{}.txt".format(PROBLEM_ID), "a")
    file.write("%s \t %s \t %s \t %s\n" % ("State   ",H1,H2,"Diff     "))
    U_2norm = 0.0
    U_maxnorm = -10000
    for state in U1.keys():
        U_diff[state] = U1[state] - U2[state]        
        U_2norm = U_2norm + U_diff[state]**2        
        if np.abs(U_diff[state]) > U_maxnorm:
            U_maxnorm = np.abs(U_diff[state])
        file.write("%s: \t %+.3f \t %+.3f \t %+.5f\n" % (state,U1[state],U2[state],U_diff[state]))
    file.write("\n")    
    file.write("Max norm: %.5f\n" % (U_maxnorm))     
    file.write("2-norm  : %.5f\n" % (U_2norm))
    file.close()    
    return U_diff,U_2norm,U_maxnorm


def value_iteration(epsilon=0.001):
    """
    Value iteration algorithm, used to compare the "true" utility values
    with the one compared with the Q-agent
    """
    U1 = dict([(s, 0) for s in range(64)])

    R, T, gamma = Rew, env_qlearn.P, GAMMA
    while True:
        U = U1.copy()
        delta = 0
        for s in range(64):
            U1[s] = Rew(s) + gamma * max([sum([p * U[s1] for (p, s1, a, b) in T[s][a]])
                                        for a in range(env_qlearn.action_space.n)])
            delta = max(delta, abs(U1[s] - U[s]))
        if delta < epsilon * (1 - gamma) / gamma:
             return U


U_vi = value_iteration(epsilon=0.001)
"""
Collects and prints the results for the Random Agent and draws the graphs
Draws:
    Mean Reward per Episode vs Episode Number
"""
#random_agent = RandomAgent(env_random)
#process_data_random(env_random, random_agent, MAX_EPISODES, MAX_ITERS_PER_EPISODE, REWARD_HOLE_DEFAULT, PROBLEM_ID)
"""
Collects and prints the results for the Simple Agent and draws the graphs
"""
#simple_agent = SimpleAgent(env_simple)
#process_data_simple(env_simple, simple_agent, PROBLEM_ID)
"""
Collects and prints the results for the Q-learning Agent and draws the graphs.
Draws:
    Mean Reward per Episode vs Episode Number
    Utility Values in each State against Episode Number
"""
states = [i for i in range(64)]
q_learning_agent = QLearningAgent(env_qlearn, NE, RPLUS, GAMMA, ALPHA)
U = process_data_q(env_qlearn, q_learning_agent, MAX_EPISODES,
               MAX_ITERS_PER_EPISODE, states, PROBLEM_ID, REWARD_HOLE_Q)
compare_utils(U_vi, U, 'Value itr','Q learning')