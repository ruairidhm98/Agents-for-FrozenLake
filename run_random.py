"""
  Script which creates an instance of a problem specified in the
  LochLomondEnv class and uses a random agent to attempt to solve
  the problem for a number of attempts. The results are then
  plotted as a line chart and the mean time taken for each episode
  and standard deviation of the time is printed to the stdout
"""
import sys
import time
import matplotlib.pyplot as plt
import numpy as np
from uofgsocsai import LochLomondEnv
from agent import Agent

# Reads command line argument and stores # in PROBLEM_ID,
# to specify the problem if this hasnt been provided, then
# just set a deafult
if len(sys.argv) == 2:
    PROBLEM_ID = int(sys.argv[1])
else:
    PROBLEM_ID = 0

MAX_EPISODES = 50
MAX_ITERS_PER_EPISODE = 50
REWARD_HOLE = 0.0

# Reset the random generator to a known state (for reproducability)
np.random.seed(12)

class RandomAgent(Agent):
    """
    Class to represent an agent which takes random actions in order
    to attempt to try and solve the LochLomondEnv problem
    """
    def solve(self, max_episodes, max_iter_per_episode, reward_hole):
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
        times = []
        # iterate over the episodes
        for i in range(max_episodes):
            # reset the state of the env to the starting state
            observation = self.env.reset()
            start = time.time()
            for j in range(max_iter_per_episode):
                # for debugging/develeopment you may want to visualize the individual
                # steps by uncommenting this line
                self.env.render()
                # takes a random action from the set of actions
                action = self.env.action_space.sample()
                # observe and collect the rewards as well as some
                # other meta data
                observation, reward, done, info = self.env.step(action)
                rewards[i].append(reward)
                print("i, iter, reward, done = {0} {1} {2} {3}".format(i, j, reward, done))
                # iff we are done and we have fallen in a hole
                # then render the environement, we don't exit the
                # loop in order to keep all the lists the same size for
                # computng statistics later on
                if done and reward == reward_hole:
                    end = time.time()
                    times.append(end-start)
                    self.env.render()
                    print("We have reached a hole :-( [we can't move so stop trying; just give up]")
                # iff we are done and we have reached the goal
                # state, then render environment
                if done and reward == +1.0:
                    end = time.time()
                    times.append(end-start)
                    self.env.render()
                    print("We have reached the goal :-) [stop trying to move; we can't]."
                          "That's ok we have achived the goal]")

        return (rewards, times)

# Create the random agent and then "solve" the problem
RANDOM_AGENT = RandomAgent(PROBLEM_ID, True, REWARD_HOLE)
rewards, times = RANDOM_AGENT.solve(MAX_EPISODES, MAX_ITERS_PER_EPISODE, REWARD_HOLE)
# convert the list representation to an array to perform statistics
# using numpy functions
rewards_array = np.array(rewards)
# Compute the mean vector from the results and the covariance matrix
mean_rewards = np.mean(rewards_array, axis=0)
cov = np.cov(mean_rewards)
iters = [i for i in range(MAX_ITERS_PER_EPISODE)]

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
MEAN_TIME = np.mean(times)
COV_TIME = np.std(times)

print("Mean Time:          {0}".format(MEAN_TIME))
print("Standard Deviation: {0}".format(COV_TIME))
