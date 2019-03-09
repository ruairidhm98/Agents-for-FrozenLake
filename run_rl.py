"""
Script which contains a class to represent a Q-learning function that is trying
to solve the LochLomondEnv problem. Takes a single command line argument which
specifies the problem ID for the environment
"""

import sys
import random
from pprint import pprint
from collections import defaultdict
from rl_helpers import (
    MDP, GridMDP
)
from uofgsocsai import LochLomondEnv
from utils import argmax

# Read in command line argument to find the problem id
if len(sys.argv) == 2:
    PROBLEM_ID = int(sys.argv[1])
else:
    PROBLEM_ID = 0

env = LochLomondEnv(PROBLEM_ID, True, -1.0)
goal_states = []
starting_state = None
reward_desc = [[None for i in range(env.desc.shape[0])]
               for j in range(env.desc.shape[1])]

# Get the reward for each state and put it in the necessary
# index into the list
for i in range(8):
    for j in range(8):
        # A hole, so set reward in that state to be -1.0
        if env.desc[i][j] == b'H':
            reward_desc[i][j] = -1.0
        # The goal state, so set the reward in that state to be +1.0
        elif env.desc[i][j] == b'G':
            goal_states.append((i, j))
            reward_desc[i][j] = +1.0
            # This is just an ordinary square, which there is no reward being in
        # The starting state
        elif env.desc[i][j] == b'S':
            starting_states = ((i, j))
            reward_desc[i][j] = 0.0
        else:
            reward_desc[i][j] = 0.0


class QLearningAgent:
    """
    TAKEN FROM AIMA TOOLBOX
    An exploratory Q-learning agent. It avoids having to learn the transition
    model because the Q-value of a state can be related directly to those of
    its neighbors. [Figure 21.8]
    """

    def __init__(self, mdp, Ne, Rplus, alpha=None):

        self.gamma = mdp.gamma
        self.terminals = mdp.terminals
        self.all_act = mdp.actlist
        self.Ne = Ne  # iteration limit in exploration function
        self.Rplus = Rplus  # large value to assign before iteration limit
        self.Q = defaultdict(float)
        self.Nsa = defaultdict(float)
        self.s = None
        self.a = None
        self.r = None

        if alpha:
            self.alpha = alpha
        else:
            self.alpha = lambda n: 1./(1+n)  # udacity video

    def f(self, u, n):
        """ Exploration function. Returns fixed Rplus until
        agent has visited state, action a Ne number of times.
        Same as ADP agent in book."""
        if n < self.Ne:
            return self.Rplus
        else:
            return u

    def actions_in_state(self, state):
        """ Return actions possible in given state.
            Useful for max and argmax. """
        if state in self.terminals:
            return [None]
        else:
            return self.all_act

    def __call__(self, percept):
        alpha, gamma, terminals = self.alpha, self.gamma, self.terminals
        Q, Nsa = self.Q, self.Nsa
        actions_in_state = self.actions_in_state
        s, a, r = self.s, self.a, self.r
        s1, r1 = self.update_state(percept) # current state and reward;  s' and r'
        #print("this s = {0}".format(s))
        #print(a)
        #print(r)
        #print(s1)
        #print(r1)
        if s in terminals: # if prev state was a terminal state it should be updated to the reward
            Q[s, None] = r
        # corrected from the book, we check if the last action was none i.e. no prev state or a terminal state
        if a is not None:
            Nsa[s, a] += 1
            Q[s, a] += alpha(Nsa[s, a]) * (r + gamma * max(Q[s1, a1] for a1 in actions_in_state(s1)) - Q[s, a])
        # Update for next iteration
        if s in terminals:
            self.s = self.a = self.r = None
        else:
            self.s, self.r = s1, r1
            self.a = argmax(actions_in_state(s1), key=lambda a1: self.f(Q[s1, a1], Nsa[s1, a1]))
        return self.a

    def update_state(self, percept):
        """To be overridden in most cases. The default case
        assumes the percept to be of type (state, reward)."""
        return percept


def run_single_trial_verbose(agent_program, mdp, epsiode):
    """
    Execute trial for given agent_program
    and mdp. mdp should be an instance of subclass
    of mdp.MDP
    """

    def take_single_action(mdp, s, a):
        """
        Select outcome of taking action a
        in state s. Weighted Sampling.
        """
        x = random.uniform(0, 1)
        cumulative_probability = 0.0
        for probability_state in mdp.T(s, a):
            probability, state = probability_state
            cumulative_probability += probability
            if x < cumulative_probability:
                break
        return state

    current_state = mdp.init
    agent_program.s = current_state
    rewards = []
    iters = 0
    file = open("episodes/episode{0}.txt".format(epsiode), "w")
    file.write("Episode {0}\n".format(epsiode))
    # Keep trying until we have found the goal state
    while True:
        file.write("---------------\n")
        # Collect the reward for being in this state
        current_reward = mdp.R(current_state)
        rewards.append(current_reward)
        # Take in new information from our new state such as
        # the grid position and the reward
        percept = (current_state, current_reward)
        # Take the action specified in the agent program (The Q-Learning algorithm)
        next_action = agent_program(percept)
        # We are in a goal state
        if next_action is None:
            iters += 1
            break
        # Move into a new state by taking an action specified in the current policy
        # the agent is following
        current_state = take_single_action(mdp, current_state, next_action)
        file.write("{0}\n".format(percept))
        file.write("{0}\n".format(next_action))
        file.write("{0}\n".format(current_state))
        file.write("---------------\n")
        iters += 1
    file.close()
    return (rewards, iters)


mdp = GridMDP(reward_desc, goal_states, (0, 4), .9)
q_learning_agent = QLearningAgent(mdp, 100, 100, alpha=None)
for i in range(10):
    rewards, iters = run_single_trial_verbose(q_learning_agent, mdp, i)
