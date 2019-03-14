"""
Script which drawst the graphs using the rewards collected from each of the agents
episodes
"""

import matplotlib.pyplot as plt
from scipy.interpolate import make_interp_spline, BSpline

def draw_mean_rewards(rewards, num_episodes, agent, problem_id):
    """
    Draws the graph of the mean reward against
    the episode number
    """
    episode_axis = [i for i in range(num_episodes)]
    plt.rc('figure', figsize=(8.0, 4.0), dpi=140)
    fig = plt.figure()
    fig.suptitle("Mean reward for each episode against iteration count\nProblem ID: {} Agent: {}".format(problem_id, agent))
    ax = fig.add_subplot(1, 1, 1)
    plt.ylim([-1.75, 1.0])
    ax.plot(episode_axis, rewards, label='k5', marker='.')
    ax.set_xlabel("Episode Number")
    ax.set_ylabel("Mean Reward")
    ax.grid(True)
    plt.show()
