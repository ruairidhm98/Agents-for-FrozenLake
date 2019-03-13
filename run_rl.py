"""
Script which contains a class to represent a Q-learning function that is trying
to solve the LochLomondEnv problem. Takes a single command line argument which
specifies the problem ID for the environment
"""
import sys
from collections import defaultdict
import numpy as np
from draw_graphs import draw_mean_rewards
from file_io_helpers import write_goal_episodes, write_to_file_results, write_to_file_init_states
from process_data import get_s_h_g_states
from uofgsocsai import LochLomondEnv
from utils import argmax
from solve_trial import run_single_trial_q


if len(sys.argv) == 2:
    PROBLEM_ID = int(sys.argv[1])
else:
    PROBLEM_ID = 0


class QLearningAgent:
    """
    TAKEN FROM LAB 7-RL
    An exploratory Q-learning agent. It avoids having to learn the transition
    model because the Q-value of a state can be related directly to those of
    its neighbors. [Figure 21.8]
    """

    def __init__(self, env, Ne, Rplus, alpha, gamma):
        """
        Constructor. Creates a new active learning agent that
        uses Q-learning to decide which actions to take
        """

        self.gamma = gamma
        index = np.where(env.desc == b'G')
        holes = np.where(env.desc == b'H')
        row, col = index[0][0], index[1][0]
        # Get all the terminal states including the holes
        self.terminals = []
        self.terminals = [row*8 + col]
        for i in range(len(holes[0])):
            row, col = holes[0][i], holes[1][i]
            self.terminals += [row*8 + col]
        self.all_act = [act for act in range(env.action_space.n)]
        # Iteration limit in exploration function
        # Large value to assign before iteration limit
        self.Ne, self.Rplus = Ne, Rplus
        # Q-values stored within a dictionary
        self.Q = np.zeros(
            (env.observation_space.n, env.action_space.n,), dtype=np.float64)
        # The frequency of each state action pair represented as a
        # dictionary
        self.Nsa = np.zeros(
            (env.observation_space.n, env.action_space.n,), dtype=np.int32)
        start = np.where(env.desc == b'S')
        row, col = start[0][0], start[1][[0]]
        self.s = row*8 + col
        self.a = None
        self.r = 0.0
        self.alpha = alpha

    def f(self, u, n):
        """
        Exploration function. Returns fixed Rplus until
        agent has visited state, action a Ne number of times.
        Same as ADP agent in book.
        """
        if n < self.Ne:
            return self.Rplus
        else:
            return u

    def actions_in_state(self, state):
        """
        Return actions possible in given state.
        Useful for max and argmax.
        """
        if state in self.terminals:
            return [None]
        else:
            return self.all_act

    def __call__(self, action, percept, state):
        """
        The Q-learning algorithm. Updates the Q value for a particular state
        upon every iteration of the algorithm. Returns the action which the
        agent should take according to its known Q-values
        """
        self.Nsa[state, action] += 1
        s1, r1 = percept
        predict = self.Q[s1, action]
        target = r1 + self.gamma * np.max(self.Q[s1, :])
        self.Q[state, action] = self.Q[s1, action] + \
            self.alpha * (target - predict)

    def choose_action(self, state):
        """
        Choose the action in state s with the highest Q-value
        """
        return np.argmax(self.Q[state, :])


def process_data_q(env, agent_program, max_episodes, max_iters_per_episode, states_to_graph, problem_id, reward_hole):
    """
    Plots the utility estimates for each state in the LochLomondEnv.
    Returns the results collected from run_n_trials for further
    use
    """
    # Keeps track of all the mean reward from each epsiode, use numpy for efficiency purposes
    mean_rewards = np.zeros((max_episodes,), dtype=np.float64)
    # Keeps track of the iterations per episode
    iters = np.zeros((max_episodes,), dtype=np.int32)
    # Keeps track of the amount of times the agent reached the goal
    num_goal_reached = np.zeros((max_episodes,), dtype=np.int32)
    graphs = {state: [] for state in states_to_graph}
    # Run no_of_iterations amount of episodes
    for i in range(max_episodes):
        # Collect the rewards and iteration count for the current episode
        temp_rewards, iters[i], goal = run_single_trial_q(
            env, agent_program, max_iters_per_episode, reward_hole)
        # Compute the mean reward for the episode
        mean_rewards[i] = np.mean(temp_rewards)
        if goal:
            num_goal_reached[i] = 1
        U = defaultdict(lambda: -1000.)
        # Collect all the utility values in a dictionary from the current trial,
        # updating the values if a higher utility has been found
        state = 0
        for iter_i in range(agent_program.Q.shape[0]):
            value = np.max(agent_program.Q[iter_i, :])
            if U[state] < value:
                U[state] = value
            state += 1
    # Plot the graph of mean rewards (performance measure) against episode number
    draw_mean_rewards(mean_rewards, max_episodes, "Q-Learning", problem_id)
    # Get the starting state and goal state indexes in order to write to file
    start_index = np.where(env.desc == b'S')
    row, col = start_index[0][0], start_index[1][0]
    start = "({}, {})".format(row, col)
    end_index = np.where(env.desc == b'G')
    row, col = end_index[0][0], end_index[1][0]
    goal = "({}, {})".format(row, col)
    # Write to the open file, some statistics relating to the trial for
    # further analysis
    file = open("out_qagent_{}.txt".format(problem_id), "w")
    write_to_file_init_states(file, problem_id, start, goal)
    write_to_file_results(file, mean_rewards, reward_hole,
                          max_episodes, max_iters_per_episode, iters, num_goal_reached)
    write_goal_episodes(file, num_goal_reached, max_episodes)
    file.close()
    return U
