"""
Script which contains a class to represent a Q-learning function that is trying
to solve the LochLomondEnv problem. Takes a single command line argument which
specifies the problem ID for the environment
"""

import sys
import random
from collections import defaultdict
from mdp import (
    MDP, GridMDP
)
from uofgsocsai import LochLomondEnv
from utils import argmax

# Read in command line argument to find the problem id
if len(sys.argv) == 2: PROBLEM_ID = int(sys.argv[1])
else: PROBLEM_ID = 0

class QLearningAgent:
    """
    TAKEN FROM AIMA TOOLBOX AND ADPATED SLIGHTLY
    An exploratory Q-learning agent. It avoids having to learn the transition
    model because the Q-value of a state can be related directly to those of
    its neighbors. [Figure 21.8]
    """

    def __init__(self, problem_id, Ne, Rplus, alpha=None):
        self.env = LochLomondEnv(problem_id, True, -1.0)
        goal_states = []
        reward_desc = [[None for i in range(self.env.desc.shape[0])] 
                        for j in range(self.env.desc.shape[1])]
        # Get the reward for each state and put it in the necessary
        # index into the list
        for i in range(8):
            for j in range(8):
                # A hole, so set reward in that state to be -1.0
                if self.env.desc[i][j] == b'H':
                    reward_desc[i][j] = -1.0
                # The goal state, so set the reward in that state to be +1.0
                elif self.env.desc[i][j] == b'G':
                    goal_states.append((i, j))
                    reward_desc[i][j] = +1.0
                # This is just an ordinary square, which there is no reward being in
                else:
                    reward_desc[i][j] = 0.0
        from pprint import pprint
        # Create a new GridMDP instance to model the stochastic nature of the
        # environment
        self.mdp = GridMDP(grid=reward_desc, terminals=goal_states)
        # Iteration limit in exploration function
        self.Ne = Ne
        # Large value to assign before iteration limit
        self.Rplus = Rplus
        # Q-values represented as a dictionary
        self.Q = defaultdict(float)
        self.Nsa = defaultdict(float)
        # gamma is the discounting reward factor for use in the Bellman equation
        # and terminals is our terminal states (goal state)
        self.gamma, self.terminals = self.mdp.gamma, self.mdp.terminals;
        # A list representing all the possible actions in each state
        self.all_act = self.mdp.actlist
        self.s, self.a, self.r = None, None, None
        # The reward for being in a bad state (hole)
        self.reward_hole = -1.0
        # Set the learning rate factor to a default if not specified
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
        """
        The Q-Learning algorithm
        """
        s1, r1 = self.update_state(percept)
        Q, Nsa, s, a, r = self.Q, self.Nsa, self.s, self.a, self.r
        alpha, gamma, terminals = self.alpha, self.gamma, self.terminals
        actions_in_state = self.actions_in_state

        # We have reached a goal state, we are done
        if s in terminals:
            Q[s, None] = r1
        # Make sure we are not in the goal state
        if s is not None:
            Nsa[s, a] += 1
            # Update the Q value of the state
            Q[s, a] += alpha(Nsa[s, a]) * (r + gamma * max(Q[s1, a1] 
                for a1 in actions_in_state(s1)) - Q[s, a])
        if s in terminals:
            self.s = self.a = self.r = None
        else:
            self.s, self.r = s1, r1
            self.a = argmax(actions_in_state(s1), key=lambda a1: self.f(Q[s1, a1], Nsa[s1, a1]))
        return self.a

    def update_state(self, percept):
        """
        Returns the percept
        """
        return percept

    def run_single_trial_verbose(self):
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

        current_state = self.mdp.init
        # Keep trying until we have found the goal state
        while True:
            print("---------------")
            # Collect the reward for being in this state
            current_reward = self.mdp.R(current_state)
            # Take in new information from our new state such as
            # the grid position and the reward
            percept = (current_state, current_reward)   
            # Take the action specified in the agent program (The Q-Learning algorithm)
            next_action = self(percept)
            # We are in a goal state
            if next_action is None:
                break
            # Move into a new state by taking an action specified in the current policy
            # the agent is following
            current_state = take_single_action(self.mdp, current_state, next_action)
            print(percept)
            print(next_action)
            print(current_state)
            print("---------------")

q_learning_agent = QLearningAgent(0, 2, 5, None)
q_learning_agent.run_single_trial_verbose()