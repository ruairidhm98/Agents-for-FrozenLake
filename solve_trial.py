"""
Script which contains a function that runs a single trial for any of the agents
"""
import numpy as np

def run_single_trial(env, agent_program, reward_hole, max_iters):
    """
    Runs a single trial with the given agent program. Returns
    the rewards collected by the agent, the number of iterations
    to reach either the goal state or a hole state
    """
    rewards = []
    iters = 0
    reached_goal = False
    # Keep trying until we have found the goal state
    observation = env.reset()
    reward = 0.0
    for i in range(max_iters):
        # Take in new information from our new state such as
        # the grid position and the reward
        percept = (observation, reward)
        action = agent_program(percept)
        observation, reward, done, info = env.step(action)
        iters += 1
        rewards.append(reward)
        # We have fell in a hole, we need to try again
        if done and reward == reward_hole:
            iters += 1
            break
        # Take the action specified in the agent program (The Q-Learning algorithm)
        # We are in a goal state
        if done and reward == +1.0:
            iters += 1
            reached_goal = True
            break

    return (np.asarray(rewards, dtype=np.float64), iters, reached_goal)
