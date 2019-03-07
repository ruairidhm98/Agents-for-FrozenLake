"""
  Script which creates an instance of a problem specified in the
  LochLomondEnv class and uses a random agent to attempt to solve
  the problem for a number of attempts. The results are then
  plotted as a line chart and the mean time taken for each episode
  and standard deviation of the time is printed to the stdout
"""
import sys
import time
import numpy as np
from pprint import pprint
from constants import *
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


class RandomAgent:
    """
    Class to represent an agent which takes random actions in order
    to attempt to try and solve the LochLomondEnv problem
    """

    def __init__(self, problem_id):
        """
        Constructor to initialise the environment for the agent
        """
        self.env = LochLomondEnv(problem_id=problem_id,
                                 is_stochastic=True,
                                 reward_hole=0.0)

    def __solve(self, max_episodes, max_iter_per_episode, reward_hole):
        """
        Function which attempts to solve the LochLomondEnv
        problem based on the RandomAgent definition.
        Returns the rewards and iteration count for
        each episode
        """
        # keeps track of all the rewards collected in
        # each episode
        rewards = [[] for i in range(max_episodes)]
        # keeps track of the time to reach the goal state
        times = np.zeros((max_episodes,), dtype=np.float64)
        # used so the time is only computed once per iteration
        temp_done = 1
        # iterate over the episodes
        for i in range(max_episodes):
            # reset the state of the env to the starting state
            observation = self.env.reset()
            start = time.time()
            for j in range(max_iter_per_episode):
                # takes a random action from the set of actions
                action = self.env.action_space.sample()
                # observe and collect the rewards as well as some
                # other meta data
                observation, reward, done, info = self.env.step(action)
                rewards[i].append(reward)
                if done and reward == reward_hole:
                    if temp_done == 1:
                        end = time.time()
                        times[i] = end-start
                    temp_done = 0
                    self.env.render()
                    print(
                        "We have reached a hole :-( [we can't move so stop trying; just give up]")

                if done and reward == +1.0:
                    if temp_done == 1:
                        end = time.time()
                        times[i] = end-start
                    temp_done = 0
                    self.env.render()
                    print("We have reached the goal :-) [stop trying to move; we can't]."
                          "That's ok we have achived the goal]")

        return (rewards, times)

    def __display_results(self, rewards, times, iters):
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

    def solve_and_display(self, max_episodes, max_iter_per_episode, reward_hole):
        rewards, times = self.__solve(
            max_episodes, max_iter_per_episode, reward_hole)
        iters = [i for i in range(max_iter_per_episode)]
        self.__display_results(rewards, times, iters)


random_agent = RandomAgent(PROBLEM_ID, True, REWARD_HOLE)
random_agent.solve_and_display(
    MAX_EPISODES, MAX_ITERS_PER_EPISODE, REWARD_HOLE)
