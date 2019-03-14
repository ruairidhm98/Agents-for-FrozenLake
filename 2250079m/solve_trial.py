"""
Script which contains a function that runs a single trial for any of the agents
"""


def run_single_trial_random(env, agent_program, max_iters_per_episode, reward_hole):
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
    for i in range(max_iters_per_episode):
        # Take in new information from our new state such as
        # the grid position and the reward
        percept = (observation, reward)
        action = agent_program()
        observation, reward, done, info = env.step(action)
        rewards.append(reward)
        iters += 1
        # Allow the agent to explore further even if they fall into a hole
        if done and reward == reward_hole:
            rewards.append(reward)
            break
        # Take the action specified in the agent program (The Q-Learning algorithm)
        # We are in a goal state
        if done and reward == +1.0:
            reached_goal = True
            rewards.append(reward)
            break
    return (rewards, iters, reached_goal)

def run_single_trial_q(env, agent_program, max_iters_per_episode, reward_hole):
    """
    Execute trial for given agent_program and mdp.
    mdp should be an instance of subclass of mdp.MDP
    Writes to a file called episode<n>.txt the results
    of each trial, including actions taken in each state,
    percepts etc. Returns the number of iterations it took
    to navigate successfully
    """
    rewards = []
    agent_program.s = state = env.reset()
    iters = 0
    reward = 0.0
    reached_goal = False
    for i in range(max_iters_per_episode):
        # Take in new information from our new state such as
        # the grid position and the reward
        action = agent_program.choose_action(state)
        new_state, reward, done, info = env.step(action)
        percept = (new_state, reward)
        agent_program(action, percept, state)
        rewards.append(reward)
        iters += 1
        state = new_state
        # The agent falls in a hole
        if done and reward == reward_hole:
            rewards.append(reward)
            break
        # Take the action specified in the agent program (The Q-Learning algorithm)
        # We are in a goal state
        if done and reward == +1.0:
            reached_goal = True
            rewards.append(reward)
            break
    return (rewards, iters, reached_goal)
