"""
Script which contains a function that runs a single trial (episode) 
for a given agent program
"""

def run_single_trial(env, agent_program, max_iters_per_episode, reward_hole, goal):
    """
    Execute trial for given agent_program and environment.
    Returns the number of iterations it took
    to navigate successfully
    """
    rewards = []
    current_state = env.reset()
    iters = 0
    reward = 0.0
    reached_goal = False
    done = False
    for i in range(max_iters_per_episode):
        # Move into new state by taking the action
        percept = (current_state, reward)
        # Learning phase, update the Q value for moving into the new state
        next_action = agent_program(percept)
        rewards.append(reward)
        iters += 1
        # The episode is finished
        if next_action is None or done:
            break
        # Take the action specified in the agent program (The Q-Learning algorithm)
        current_state, reward, done, info = env.step(next_action)
    if current_state == goal:
        reached_goal = True
    return (rewards, iters, reached_goal)
