"""
Script which contains a function that runs a single trial for any of the agents
"""
import numpy as np


def run_single_trial(env, agent_program, max_iters_per_episode, reward_hole):
    """
    Execute trial for given agent_program and mdp. 
    mdp should be an instance of subclass of mdp.MDP
    Writes to a file called episode<n>.txt the results
    of each trial, including actions taken in each state,
    percepts etc. Returns the number of iterations it took
    to navigate successfully
    """
    rewards = []
    iters = 0
    observation = env.reset()
    reward = 0.0
    reached_goal = False
    temp_done = False
    for i in range(max_iters_per_episode):
        # Take in new information from our new state such as
        # the grid position and the reward
        percept = (observation, reward)
        action = agent_program(percept)
        observation, reward, done, info = env.step(action)
        iters += 1
        # Collect reward for being in the current state
        if not done:
            rewards.append(reward)
        # Collect the reward for falling in the hole
        if done and reward == reward_hole and not temp_done:
            temp_done = True
            rewards.append(reward)
        # Take the action specified in the agent program (The Q-Learning algorithm)
        # We are in a goal state
        if done and reward == +1.0:
            iters += 1
            print("I've reached the goal!")
            reached_goal = True
            break
    
    return (rewards, iters, reached_goal)
