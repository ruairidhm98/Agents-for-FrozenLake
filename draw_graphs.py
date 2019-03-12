"""
Script which drawst the graphs using the rewards collected from each of the agents
episodes
"""

import matplotlib.pyplot as plt


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
    plt.ylim([-3.5, 2.5])
    ax.plot(episode_axis, rewards, label='k5', marker='.')
    ax.set_xlabel("Episode Number")
    ax.set_ylabel("Mean Reward")
    ax.grid(True)
    plt.show()


def draw_utility_estimate_graph(graphs, problem_id):
    """
    Plots the Utilities for each state after the agent
    has run a number of trials
    """
    for state, value in graphs.items():
        state_x, state_y = zip(*value)
        plt.plot(state_x, state_y, label=str(state))
    plt.ylim([-2.6, 2.6])
    plt.grid(True)
    plt.title("Estimated Utility Against Episode Count\nProblem ID: {}".format(problem_id))
    plt.Text("Each colour represents a state in the Graph")
    plt.xlabel('Iterations')
    plt.ylabel('Utility')
    plt.show()
