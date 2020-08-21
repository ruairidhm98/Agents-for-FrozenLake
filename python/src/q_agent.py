"""
Script which contains a class to represent a Q-learning agent that is trying
to solve the LochLomondEnv problem.
"""
from collections import defaultdict
from random import randint
import numpy as np
from draw_graphs import draw_mean_rewards
from file_io_helpers import (write_goal_episodes, write_to_file_init_states,
                             write_to_file_results)
from solve_trial import run_single_trial
from utils import argmax


class QLearningAgent:
    """
    TAKEN FROM LAB 7-RL
    An exploratory Q-learning agent. It avoids having to learn the transition
    model because the Q-value of a state can be related directly to those of
    its neighbors. AIMA [Figure 21.8]
    """

    def __init__(self, env, Ne, Rplus, gamma, alpha):
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
            self.terminals.append([row*8 + col])
        self.all_act = [act for act in range(env.action_space.n)]
        # Iteration limit in exploration function
        # Large value to assign before iteration limit
        self.Ne, self.Rplus = Ne, Rplus
        # Q-values stored within a dictionary
        self.Q = defaultdict(float)
        # The frequency of each state action pair represented as a
        # dictionary
        self.Nsa = defaultdict(float)
        self.s = self.a = self.r = None
        self.alpha = alpha

    def f(self, u, n):
        """
        Exploration function. Returns fixed Rplus until
        agent has visited state, action a Ne number of times.
        """
        if n < self.Ne:
            return self.Rplus
        else:
            return u

    def actions_in_state(self, state):
        """
        Return actions possible in a given state.
        """
        if state in self.terminals:
            return [None]
        else:
            return self.all_act

    def __call__(self, percept):
        """
        The Q-learning algorithm. Updates the Q value for a particular state
        upon every iteration of the current episode. Returns the action which the
        agent should take according to its known Q-values and exploration limit
        """
        alpha, gamma, terminals = self.alpha, self.gamma, self.terminals
        Q, Nsa = self.Q, self.Nsa
        actions_in_state = self.actions_in_state
        s, a, r = self.s, self.a, self.r
        # Current state and reward;  s' and r'
        s1, r1 = percept
        # If prev state was a terminal state it should be updated to the reward
        if s in terminals:
            Q[s, None] = r
        # Check if the last action was none i.e. no prev state or a
        # terminal state, if it is not, then update the Q-value for
        # that state and action
        if a is not None:
            Nsa[s, a] += 1
            # Select the action which produces the maximum Q-value in state s
            Q[s, a] += alpha * (r + gamma * max(Q[s1, a1] for a1 in actions_in_state(s1)) - Q[s, a])
        # Update for next iteration
        if s in terminals:
            self.s = self.a = self.r = None
        else:
            self.s, self.r = s1, r1
            # Choose the action depending on how much the agent has explored
            # state s and taking action a and its current Q value for that state
            self.a = argmax(actions_in_state(s1), key=lambda a1: self.f(Q[s1, a1], Nsa[s1, a1]))
            # If the next action is none and we are not in a terminal state, then just take
            # a random action
            if self.a is None and s not in terminals:
                self.a = randint(0, 3)
        return self.a

def process_data_q(env, agent_program, max_episodes, max_iters_per_episode, states_to_graph, problem_id, reward_hole):
    """
    Runs the problem a number of times, collects results and writes
    to file some statistics from the experiments and plots the graph
    of mean reward per episode vs episode number. Returns the utilities
    of each state curretly known by the agent after it executes the
    episodes of the problem.
    """
    # Keeps track of all the mean rewards from each epsiode
    mean_rewards = np.zeros((max_episodes,), dtype=np.float64)
    # Keeps track of the iterations per episode
    iters = np.zeros((max_episodes,), dtype=np.int32)
    # Keeps track of the amount of times the agent reached the goal
    num_goal_reached = np.zeros((max_episodes,), dtype=np.int32)
    graphs = {state: [] for state in states_to_graph}
    goal = np.where(env.desc == b'G')
    row_g, col_g = goal[0][0], goal[1][0]
    goal_state = row_g*8 + col_g
    # Run no_of_iterations amount of episodes
    for i in range(max_episodes):
        # Collect the rewards and iteration count for the current episode
        temp_rewards, iters[i], goal = run_single_trial(
            env, agent_program, max_iters_per_episode, reward_hole, goal_state)
        # Compute the mean reward for the episode
        mean_rewards[i] = np.mean(temp_rewards)
        if goal:
            num_goal_reached[i] = 1
        U = defaultdict(lambda: -1000.)
        # Collect all the utility values in a dictionary from the current trial,
        # updating the values if a higher utility has been found
        for state_action, value in agent_program.Q.items():
            state, action = state_action
            if U[state] < value:
                U[state] = value
    # Plot the graph of mean rewards (performance measure) against episode number
    draw_mean_rewards(mean_rewards, max_episodes, "Q-Learning", problem_id)
    # Get the starting state and goal state indexes in order to write to file
    start_index = np.where(env.desc == b'S')
    row, col = start_index[0][0], start_index[1][0]
    start = "({}, {})".format(row, col)
    goal = "({}, {})".format(row_g, col_g)
    # Write to the open file, some statistics relating to the trial for
    # further analysis
    file = open("out_qagent_{}.txt".format(problem_id), "w")
    write_to_file_init_states(file, problem_id, start, goal)
    write_to_file_results(file, mean_rewards, reward_hole,
                          max_episodes, max_iters_per_episode, iters, num_goal_reached)
    write_goal_episodes(file, num_goal_reached, max_episodes)
    file.close()
    return U
