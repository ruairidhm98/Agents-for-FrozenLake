"""
Script which creates an instance of a problem specified in the
LochLomondEnv class and uses a random agent to attempt to solve
the problem for a number of attempts. The results are then
plotted as a line chart and the mean time taken for each episode
and standard deviation of the time is printed to the stdout
"""
import sys
import numpy as np
from pprint import pprint
import matplotlib.pyplot as plt
from solve import run_single_trial
from uofgsocsai import LochLomondEnv
from draw_graphs import draw_mean_rewards
from file_io_helpers import write_goal_episodes

# Reads command line argument and stores # in PROBLEM_ID,
# to specify the problem if this hasnt been provided, then
# just set a deafult
if len(sys.argv) == 2:
    PROBLEM_ID = int(sys.argv[1])
else:
    PROBLEM_ID = 0

REWARD_HOLE = 0.0

rand_file = open("out_random_{}.txt".format(PROBLEM_ID), "w")
rand_file.write("Problem ID: {}\n".format(PROBLEM_ID))
rand_file.write("Reward Hole: {}\n".format(REWARD_HOLE))

# Reset the random generator to a known state (for reproducability)
np.random.seed(12)
env = LochLomondEnv(PROBLEM_ID, is_stochastic=True, reward_hole=0.0)


class RandomAgent:
    """
    Class to represent an agent which takes random actions in order
    to attempt to try and solve the LochLomondEnv problem
    """

    def __call__(self):
        """
        Agent program, returns a random action to be taken
        """
        return env.action_space.sample()


def process_data_random(agent_program, max_episodes, max_iter_per_episode, reward_hole):
    """
    Solves the problem using the agent program passed in as a parameter
    """
    # Keep track of the mean reward collected in each episode
    mean_rewards = np.zeros((max_episodes), dtype=np.float64)
    # Keep track of the iteration count for each episode
    iters = np.zeros((max_episodes,), dtype=np.int32)
    # Keeps track of the times the agent reached the goal
    num_goal = np.zeros((max_episodes,), dtype=np.int32)
    # Run a specified number of episodes and collect the rewards and iteration
    # count for data analysis
    for i in range(max_episodes):
        temp_rewards, iters[i], reached_goal = run_single_trial(
            env, agent_program, reward_hole, max_iter_per_episode)

        mean_rewards = np.mean(temp_rewards)
        if reached_goal:
            num_goal[i] = 1

    file = open("out_random_{}.txt".format(PROBLEM_ID), "w")
    file.write(
        "Reached The Goal State: {0}/{1}".format(num_goal, max_episodes))
    
    write_goal_episodes(rand_file, num_goal)
    draw_mean_rewards(mean_rewards, max_episodes)
