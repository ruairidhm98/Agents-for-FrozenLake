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
            starting_state = ((i, j))
            reward_desc[i][j] = 0.0
        else:
            reward_desc[i][j] = 0.0
#print(reward_desc)
#print(env.desc[0][7])
class QLearningAgent:
    """
    TAKEN FROM AIMA TOOLBOX
    An exploratory Q-learning agent. It avoids having to learn the transition
    model because the Q-value of a state can be related directly to those of
    its neighbors. [Figure 21.8]
    """

    def __init__(self, mdp, Ne, Rplus, alpha=None):
        """
        Constructor. Creates a new active learning agent that
        uses Q-learning to decide which actions to take
        """
        self.gamma = mdp.gamma
        self.terminals = mdp.terminals
        self.all_act = mdp.actlist
        # iteration limit in exploration function
        self.Ne = Ne
        # large value to assign before iteration limit
        self.Rplus = Rplus
        self.Q = defaultdict(float)
        self.Nsa = defaultdict(float)
        self.s = None
        self.a = None
        self.r = None

        if alpha:
            self.alpha = alpha
        # udacity video
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
        # current state and reward;  s' and r'
        s1, r1 = self.update_state(percept)
        # if prev state was a terminal state it should be updated to the reward
        if s in terminals:
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


def run_single_trial_verbose(agent_program, mdp, episode):
    """
    Execute trial for given agent_program and mdp. 
    mdp should be an instance of subclass of mdp.MDP
    Writes to a file called episode<n>.txt the results
    of each trial, including actions taken in each state,
    percepts etc. Returns the number of iterations it took
    to navigate successfully
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
    if episode == 100000:
        file = open("episodes/episode{0}.txt".format(episode), "w")
        file.write("Episode {0}\n".format(episode))
    # Keep trying until we have found the goal state
    while True:
        if episode == 100000:
            file.write("---------------\n")
        # Collect the reward for being in this state
        current_reward = mdp.R(current_state)
        rewards.append(current_reward)
        # Take in new information from our new state such as
        # the grid position and the reward
        percept = (current_state, current_reward)
        if episode == 100000:
            file.write("{0}\n".format(percept))
            file.write("{0}\n".format(current_state))
            file.write("---------------\n")
        # We have fell in a hole, we need to try again
        if current_reward == -1.0:
            iters += 1
            if episode == 100000:
                file.write("Reached a hole. Give up\n")
            break
        # Take the action specified in the agent program (The Q-Learning algorithm)
        next_action = agent_program(percept)
        if episode == 100000:
            file.write("{0}\n".format(next_action))
        # We are in a goal state
        if next_action is None:
            iters += 1
            if episode == 100000:
                file.write("Reached the Goal!\n")
            break
        # Move into a new state by taking an action specified in the current policy
        # the agent is following
        current_state = take_single_action(mdp, current_state, next_action)
        iters += 1

    if episode == 100000:
        file.write("Iterations {0}\n".format(iters))
        file.write("Rewards: {0}\n".format(rewards))
        file.close()
    return (rewards, iters)

mdp = GridMDP(reward_desc, goal_states, starting_state, .9)
q_learning_agent = QLearningAgent(mdp, 5, 2, alpha= lambda n: 60./59+n)
for i in range(100001):
    rewards, iters = run_single_trial_verbose(q_learning_agent, mdp, i)
