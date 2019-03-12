"""
Script which contains a class to represent a Q-learning function that is trying
to solve the LochLomondEnv problem. Takes a single command line argument which
specifies the problem ID for the environment
"""
import sys
from collections import defaultdict
import numpy as np
from draw_graphs import draw_mean_rewards, draw_utility_estimate_graph
from file_io_helpers import write_goal_episodes, write_to_file_results, write_to_file_init_states
from solve_trial import run_single_trial
from uofgsocsai import LochLomondEnv
from utils import argmax


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

    def __init__(self, env, Ne, Rplus, alpha):
        """
        Constructor. Creates a new active learning agent that
        uses Q-learning to decide which actions to take
        """
        self.gamma = 0.9
        index = np.where(env.desc == b'G')
        row, col = index[0][0], index[1][0]
        self.terminals = [row*8 + col]
        self.all_act = [act for act in range(env.action_space.n)]
        # Iteration limit in exploration function
        # Large value to assign before iteration limit
        self.Ne, self.Rplus = Ne, Rplus
        self.Q = defaultdict(float)
        self.Nsa = defaultdict(float)
        self.s = self.a = self.r = None
        if alpha:
            self.alpha = alpha
        else:
            self.alpha = lambda n: 60./(59+n)

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

    def __call__(self, percept):
        """
        The Q-learning algorithm. Updates the Q value for a particular state
        upon every iteration of the algorithm. Returns the action which the
        agent should take according to its known Q-values
        """
        alpha, gamma, terminals = self.alpha, self.gamma, self.terminals
        Q, Nsa = self.Q, self.Nsa
        actions_in_state = self.actions_in_state
        s, a, r = self.s, self.a, self.r
        # Current state and reward;  s' and r'
        s1, r1 = self.update_state(percept)
        # If prev state was a terminal state it should be updated to the reward
        if s in terminals:
            Q[s, None] = r
        # Corrected from the book, we check if the last action was none i.e. no prev state or a terminal state
        if a is not None:
            Nsa[s, a] += 1
            Q[s, a] += alpha(Nsa[s, a]) * (r + gamma * argmax(Q[s1, a1] for a1 in actions_in_state(s1)) - Q[s, a])
        # Update for next iteration
        if s in terminals:
            self.s = self.a = self.r = None
        else:
            self.s, self.r = s1, r1
            self.a = argmax(actions_in_state(
                s1), key=lambda a1: self.f(Q[s1, a1], Nsa[s1, a1]))
        return self.a

    def update_state(self, percept):
        """
        To be overridden in most cases. The default case
        assumes the percept to be of type (state, reward).
        """
        return percept


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
        temp_rewards, iters[i], goal = run_single_trial(
            env, agent_program, max_iters_per_episode, reward_hole)
        # Compute the mean reward for the episode
        mean_rewards[i] = np.mean(temp_rewards)
        if goal: num_goal_reached[i] = 1
        U = defaultdict(lambda: -1000.)
        # Collect all the utility values in a dictionary from the current trial,
        # updating the values if a higher utility has been found
        for state_action, value in agent_program.Q.items():
            state, action = state_action
            if U[state] < value:
                U[state] = value

        for state in states_to_graph:
            graphs[state].append((i, U[state]))
    # Plot the graph of mean rewards (performance measure) against episode number
    draw_mean_rewards(mean_rewards, max_episodes, "Q-Learning", problem_id)
    # Plot the utility of each state on the graph using a separate colour
    # for each state
    draw_utility_estimate_graph(graphs, problem_id)
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
