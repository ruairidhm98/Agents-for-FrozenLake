"""
Script which contains a class to represent a Q-learning function that is trying
to solve the LochLomondEnv problem. Takes a single command line argument which
specifies the problem ID for the environment
"""
import sys
from collections import defaultdict
import numpy as np
import matplotlib.pyplot as plt
from utils import argmax
from uofgsocsai import LochLomondEnv

# Read in command line argument to find the problem id
if len(sys.argv) == 2:
    PROBLEM_ID = int(sys.argv[1])
else:
    PROBLEM_ID = 0

REWARD_HOLE = -5.00
file = open("out_qagent_{}_epsiodes.txt".format(PROBLEM_ID), "w")
env = LochLomondEnv(PROBLEM_ID, is_stochastic=True, reward_hole=REWARD_HOLE)
file.write("Problem ID: {}\n".format(PROBLEM_ID))
file.write("Reward Hole: {}\n".format(REWARD_HOLE))

class QLearningAgent:
    """
    TAKEN FROM LAB 7-RL
    An exploratory Q-learning agent. It avoids having to learn the transition
    model because the Q-value of a state can be related directly to those of
    its neighbors. [Figure 21.8]
    """

    def __init__(self, Ne, Rplus, alpha=None):
        """
        Constructor. Creates a new active learning agent that
        uses Q-learning to decide which actions to take
        """
        self.gamma = 0.9
        index = np.where(env.desc == b'G')
        row, col = index[0][0], index[1][0]
        self.terminals = [row*8 + col]
        self.all_act = [act for act in range(env.action_space.n)]
        # iteration limit in exploration function
        self.Ne, self.Rplus = Ne, Rplus
        # large value to assign before iteration limit
        self.Q_table = defaultdict(float)
        self.Nsa = defaultdict(float)
        self.state = self.action = self.reward = None

        if alpha:
            self.alpha = alpha
        else:
            self.alpha = lambda n: 1./(1+n)

    def f(self, u, n):
        """
        Exploration function. Returns fixed Rplus until
        agent has visited state, action a Ne number of times.
        Same as ADP agent in book.
        """
        if n < self.Ne:
            return self.Rplus
        return u

    def actions_in_state(self, state):
        """
        Return actions possible in given state.
        Useful for max and argmax.
        """
        if state in self.terminals:
            return [None]
        return self.all_act

    def __call__(self, percept):
        """
        Agent Program (The Q-learning algorithm). Updates the Q value for a particular state
        upon every iteration of the algorithm. Returns the action which the
        agent should take according to its known Q-values
        """
        alpha, gamma, terminals = self.alpha, self.gamma, self.terminals
        Q_table, Nsa = self.Q_table, self.Nsa
        actions_in_state = self.actions_in_state
        state, action, reward = self.state, self.action, self.reward
        # current state and reward;  s' and r'
        s1, r1 = self.update_state(percept)
        # if prev state was a terminal state it should be updated to the reward
        if state in terminals:
            Q_table[state, None] = reward
        # corrected from the book, we check if the last action was none i.e. no prev state
        # or a terminal state
        if action is not None:
            Nsa[state, action] += 1
            Q_table[state, action] += alpha(Nsa[state, action]) * (reward + gamma * max(
                Q_table[s1, a1] for a1 in actions_in_state(s1)) - Q_table[state, action])
        # Update for next iteration
        if state in terminals:
            self.state = self.action = self.reward = None
        else:
            self.state, self.reward = s1, r1
            self.action = argmax(actions_in_state(
                s1), key=lambda a1: self.f(Q_table[s1, a1], Nsa[s1, a1]))
        return self.action

    def update_state(self, percept):
        """
        To be overridden in most cases. The default case
        assumes the percept to be of type (state, reward).
        """
        return percept


def run_n_trials(agent_program, max_iters_per_episode):
    """
    Execute trial for given agent_program and mdp.
    mdp should be an instance of subclass of mdp.MDP
    Writes to a file called episode<n>.txt the results
    of each trial, including actions taken in each state,
    percepts etc. Returns the number of rewards collected
    in each iteration, the number of iterations it took to
    either fall in a hole or each the goal to navigate
    successfully to the goal and a boolean indicating if the
    goal was reached
    """
    rewards = []
    iters = 0
    reached_goal = False
    # Keep trying until we have found the goal state
    observation = env.reset()
    reward = 0.0
    for i in range(max_iters_per_episode):
        # Take in new information from our new state such as
        # the grid position and the reward
        percept = (observation, reward)
        action = agent_program(percept)
        observation, reward, done, info = env.step(action)
        iters += 1
        rewards.append(reward)
        # We have fell in a hole, we need to try again
        if done and reward == REWARD_HOLE:
            iters += 1
            break
        # Take the action specified in the agent program (The Q-Learning algorithm)
        # We are in a goal state
        if done and reward == +1.0:
            iters += 1
            reached_goal = True
            break

    return (np.asarray(rewards, dtype=np.float64), reached_goal)


def draw_mean_rewards(rewards, num_episodes):
    """
    Draws the graph of the mean reward against
    the episode number
    """
    # Compute the mean vector from the results and the covariance matrix
    cov_rewards = np.cov(rewards)
    file.write("Covariance of Rewards: {}\n".format(cov_rewards))
    episode_axis = [i for i in range(num_episodes)]
    # Plot the mean vector against iteration count
    plt.rc('figure', figsize=(8.0, 4.0), dpi=140)
    fig = plt.figure()
    fig.suptitle("Mean reward for each episode against iteration count")
    ax = fig.add_subplot(1, 1, 1)
    ax.plot(episode_axis, rewards, label='k5', marker='.')
    ax.set_xlabel("Episode Number")
    ax.set_ylabel("Mean Reward")
    ax.grid(True)
    plt.show()


def process_data(agent_program, no_of_iterations, states_to_graph):
    """
    Plots the utility estimates for each state in the LochLomondEnv.
    Returns the results collected from run_n_trials for further
    use
    """
    # Keeps track of all the mean reward from each epsiode, use numpy for efficiency purposes
    mean_rewards = np.zeros((no_of_iterations,), dtype=np.float64)
    # The maximum of number of iterations the agent can do in each episode
    max_iters_per_episode = 100
    # Keeps track of the amount of times the agent reached the goal
    num_goal_reached = np.zeros((no_of_iterations,), dtype=np.int32)
    graphs = {state: [] for state in states_to_graph}
    # Run no_of_iterations amount of episodes
    for iteration in range(1, no_of_iterations+1):
        # Collect the rewards and iteration count for the current episode
        temp_rewards, goal = run_n_trials(agent_program, max_iters_per_episode)
        if goal:
            num_goal_reached[iteration-1] = 1
        U = defaultdict(lambda: -1000.)
        # Collect all the utility values in a dictionary from the current trial,
        # updating the values if a higher utility has been found
        for state_action, value in agent_program.Q_table.items():
            state, action = state_action
            if U[state] < value:
                U[state] = value
        mean_rewards[iteration-1] = np.mean(temp_rewards)

        for state in states_to_graph:
            graphs[state].append((iteration, U[state]))

    # Plot the graph of mean rewards (performance measure) against episode number
    draw_mean_rewards(mean_rewards, no_of_iterations)

    # Write to the open file, some statistics relating to the trial for
    # further analysis
    goal_state = np.where(num_goal_reached == 1)
    num_goals = len(goal_state[0])
    print(goal_state)
    print(num_goals)
    file.write("Number of Times The Agent Reached The Goal: {0}/{1}\n".format(
        num_goals, no_of_iterations))
    file.write("Episodes Where Goal Was Reached:")
    # Write the episodes where the goal was reached in order to
    # analyse if an optimal path is reached (indicated by a episode
    # numbers that are close together consecutively)
    for i in range(num_goals):
        file.write(" {},".format(goal_state[0][i]))
        if i % 9 == 0 and i != num_goals-1 and i > 0:
            file.write("\n")
    file.write("\n")
    file.write("Maximum Mean Reward: {}\n".format(np.max(mean_rewards)))
    file.write("Minimum Mean Reward: {}\n".format(np.min(mean_rewards)))
    # Plot the utility of each state on the grpah using a separate colour
    # for each state
    for state, value in graphs.items():
        state_x, state_y = zip(*value)
        plt.plot(state_x, state_y, label=str(state))
    # Set some graph meta data
    plt.ylim([-2.6, 2.6])
    plt.grid(True)
    plt.title("Estimated Utility Against Episode Count")
    plt.legend(loc='lower right')
    plt.xlabel('Iterations')
    plt.ylabel('Utility')
    plt.show()


q_learning_agent = QLearningAgent(50, 40)
states = [i for i in range(64)]
process_data(q_learning_agent, 250, states)
file.close()
