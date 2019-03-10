"""
Script which contains a class to represent a Q-learning function that is trying
to solve the LochLomondEnv problem. Takes a single command line argument which
specifies the problem ID for the environment
"""
import sys
import numpy as np
from collections import defaultdict
from uofgsocsai import LochLomondEnv
from utils import argmax


# Read in command line argument to find the problem id
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

    def __init__(self, env, Ne, Rplus, alpha=None):
        """
        Constructor. Creates a new active learning agent that
        uses Q-learning to decide which actions to take
        """
        self.gamma = 0.1
        index = np.where(env.desc==b'G')
        row = index[0][0]
        col = index[1][0]
        self.terminals = [row*8 + col]
        self.all_act = [act for act in range(env.action_space.n)]
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
        """
        To be overridden in most cases. The default case
        assumes the percept to be of type (state, reward).
        """
        return percept


def run_n_trials(env, agent_program, max_episodes, max_iters_per_episode):
    """
    Execute trial for given agent_program and mdp. 
    mdp should be an instance of subclass of mdp.MDP
    Writes to a file called episode<n>.txt the results
    of each trial, including actions taken in each state,
    percepts etc. Returns the number of iterations it took
    to navigate successfully
    """
    rewards = [[] for i in range(max_episodes)]
    iters = [0 for i in range(max_episodes)]
    file = open("out_qagent_{}_epsiodes.txt".format(PROBLEM_ID), "w")
    # Keep trying until we have found the goal state
    for i in range(max_episodes):
        file.write("Episode {}\n".format(i))
        file.write("-----------------------------------------------\n")
        observation = env.reset()
        reward = 0.0
        for j in range(max_iters_per_episode):
            file.write("---------------\n")
            # Take in new information from our new state such as
            # the grid position and the reward
            percept = (observation, reward)
            # We have fell in a hole, we need to try again
            action = agent_program(percept);
            file.write("Observation: {}\n".format(observation))
            file.write("Action:      {0}\n".format(action))
            observation, reward, done, info = env.step(action)
            rewards[i].append(reward)
            if done and reward == -1.0:
                iters[i] += 1
                file.write("Reached a hole. Give up!\n")
                break
            # Take the action specified in the agent program (The Q-Learning algorithm)
            # We are in a goal state
            if done and reward == +1.0:
                iters[i] += 1
                file.write("Reached the Goal!\n")
                break
            # Move into a new state by taking an action specified in the current policy
            # the agent is following
            iters[i] += 1
            file.write("---------------\n")
        # Write to the file if agent used up all of its iterations
        # in the episode
        if iters[i] == max_iters_per_episode:
            file.write("Ran out of iterations!\n")
        file.write("Iterations: {0}\n".format(iters[i]))
        file.write("-----------------------------------------------\n")
    file.close()
    return (rewards, iters)
