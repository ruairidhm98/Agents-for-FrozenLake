"""
Script which creates an instance of a problem specified in the
LochLomondEnv class and uses a random agent to attempt to solve
the problem for a number of attempts. The results are then
plotted as a line chart and the mean time taken for each episode
and standard deviation of the time is printed to the stdout
"""
import sys
import random
import numpy as np
import matplotlib.pyplot as plt
from solve_trial import run_single_trial
from uofgsocsai import LochLomondEnv
from draw_graphs import draw_mean_rewards
from file_io_helpers import write_goal_episodes, write_to_file_results, write_to_file_init_states

# Reads command line argument and stores # in PROBLEM_ID,
# to specify the problem if this hasnt been provided, then
# just set a deafult
if len(sys.argv) == 2:
    PROBLEM_ID = int(sys.argv[1])
else:
    PROBLEM_ID = 0

REWARD_HOLE = 0.0

# Reset the random generator to a known state (for reproducability)
np.random.seed(12)


class RandomAgent:
    """
    Class to represent an agent which takes random actions in order
    to attempt to try and solve the LochLomondEnv problem
    """
    
    def __call__(self, percept):
        """
        Agent program, returns a random action to be taken
        """
        return random.randint(0, 3)


def process_data_random(envir, agent_program, max_episodes, max_iter_per_episode, reward_hole, problem_id):
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
            envir, agent_program, max_iter_per_episode, REWARD_HOLE)
        mean_rewards[i] = np.mean(temp_rewards)
        if reached_goal:
            num_goal[i] = 1
    
    # Get the starting state and goal state indexes in order to write to file
    start_index = np.where(envir.desc == b'S')
    row, col = start_index[0][0], start_index[1][0]
    start = "({}, {})".format(row, col)
    end_index = np.where(envir.desc == b'G')
    row, col = end_index[0][0], end_index[1][0]
    goal = "({}, {})".format(row, col)

    file = open("out_random_{}.txt".format(problem_id), "w")
    write_to_file_init_states(file, problem_id, start, goal)
    write_to_file_results(file, mean_rewards, REWARD_HOLE, max_episodes, max_iter_per_episode, iters, num_goal)
    write_goal_episodes(file, num_goal, max_episodes)
    draw_mean_rewards(mean_rewards, max_episodes, "Random", problem_id)
    file.close()
