import sys
from pprint import pprint
from mdp import ( 
  value_iteration, GridMDP
)
import numpy as np
import random
from uofgsocsai import LochLomondEnv
from utils import argmax
from collections import defaultdict
import time

if len(sys.argv) == 2: PROBLEM_ID = int(sys.argv[1])
else: PROBLEM_ID = 0

class QLearningAgent:
    """ 
    An exploratory Q-learning agent. It avoids having to learn the transition
    model because the Q-value of a state can be related directly to those of
    its neighbors. [Figure 21.8]
    """

    def __init__(self, problem_id, Ne, Rplus, alpha=None):

        self.env = LochLomondEnv(problem_id, True, -1.0)
        goal_states = []
        reward_desc = [[None for i in range(self.env.desc.shape[0])] for j in range(self.env.desc.shape[1])]
        for i in range(8):
            for j in range(8):
                if self.env.desc[i][j] == b'H':
                    reward_desc[i][j] = -1.0
                elif self.env.desc[i][j] == b'G':
                    goal_states.append((i,j))
                    reward_desc[i][j] = +1.0
                else:
                    reward_desc[i][j] = 0.0
        self.mdp = GridMDP(grid=reward_desc, terminals=goal_states)
        self.Ne = Ne  # iteration limit in exploration function
        self.Rplus = Rplus  # large value to assign before iteration limit
        self.Q = defaultdict(float)
        self.Nsa = defaultdict(float)
        self.gamma = self.mdp.gamma
        self.terminals = self.mdp.terminals
        self.all_act = self.mdp.actlist
        self.s = None
        self.a = None
        self.r = None
        self.reward_hole = -1.0
        self.rewar = self.mdp.reward

        if alpha: 
            self.alpha = alpha
        else: 
            self.alpha = lambda n: 1./(1+n)  # udacity video

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
        s1, r1 = self.update_state(percept)
        Q, Nsa, s, a, r = self.Q, self.Nsa, self.s, self.a, self.r
        alpha, gamma, terminals = self.alpha, self.gamma, self.terminals,
        actions_in_state = self.actions_in_state

        if s in terminals:
            Q[s, None] = r1
        if s is not None:
            Nsa[s, a] += 1
            Q[s, a] += alpha(Nsa[s, a]) * (r + gamma * max(Q[s1, a1]
                                           for a1 in actions_in_state(s1)) - Q[s, a])
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

    def run_single_trial_verbose(self):
        """Execute trial for given agent_program
        and mdp. mdp should be an instance of subclass
        of mdp.MDP """

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

        current_state = self.mdp.init
        while True:
            print("---------------")        
            current_reward = self.mdp.R(current_state)
            percept = (current_state, current_reward)        
            next_action = self(percept)
            if next_action is None:
                break
            current_state = take_single_action(self.mdp, current_state, next_action)
            print(percept)
            print(next_action)
            print(current_state)
            print("---------------")


q = QLearningAgent(0, Ne=5, Rplus=2, alpha=None)
for i in range(10): q.run_single_trial_verbose()
