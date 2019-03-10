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


# Reads command line argument and stores # in PROBLEM_ID,
# to specify the problem if this hasnt been provided, then
# just set a deafult
if len(sys.argv) == 2:
    PROBLEM_ID = int(sys.argv[1])
else:
    PROBLEM_ID = 0

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

def solve(agent_program, max_episodes, max_iter_per_episode, reward_hole):
    """
    Function which attempts to solve the LochLomondEnv
    problem based on the RandomAgent definition.
    Returns the rewards and iteration count for
    each episode
    """
    # Keeps track of all the rewards collected in
    # each episode
    rewards = [[] for i in range(max_episodes)]
    file = open("out_random_{}_trials".format(PROBLEM_ID))
    # Iterate over the episodes
    for i in range(max_episodes):
        # Reset the state of the env to the starting state
        observation = self.env.reset()
        start = time.time()
        for j in range(max_iter_per_episode):
            # Takes a random action from the set of actions
            action = agent_program()
            # Obbserve and collect the rewards as well as some
            # other meta data
            observation, reward, done, info = self.env.step(action)
            rewards[i].append(reward)
            # We have reached a hole, exit the current episode
            if done and reward == 0.0:
                file.write("Reached a hole. Give up!\n")
                break
            # We have reached the goal, exit the current
            # episode
            if done and reward == +1.0:
                file.write("Reached the Goal!\n")
                break

        return (rewards, times)

def display_results(rewards, times, iters):
    """
    Draws the graph of rewards against iteration count after solving
    the problem and also prints out the mean time taken and standard
    deviation of the times
    """
    # Compute the mean vector from the results and the covariance matrix
    mean_rewards = np.mean(rewards, axis=0)
    # Plot the mean vector against iteration count
    plt.rc('figure', figsize=(8.0, 4.0), dpi=140)
    fig = plt.figure()
    fig.suptitle("Mean reward for each episode against iteration count")
    ax = fig.add_subplot(1, 1, 1)
    ax.plot(iters, mean_rewards, label='k5', marker='.')
    ax.set_xlabel("Iteration count")
    ax.set_ylabel("Rewards")
    ax.grid(True)
    plt.show()

    # Compute the mean time and covariance for each time
    mean_time = np.mean(times)
    std_time = np.std(times)

    print("Mean Time:          {0}".format(mean_time))
    print("Standard Deviation: {0}".format(std_time))

def solve_and_display(max_episodes, max_iter_per_episode, reward_hole):
    rewards, times = self.__solve(
    max_episodes, max_iter_per_episode, reward_hole)
    iters = [i for i in range(max_iter_per_episode)]
    display_results(rewards, times, iters)
