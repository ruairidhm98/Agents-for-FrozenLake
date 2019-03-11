"""
Script which contains some helper with regards to File I/O
"""
import numpy as np


def write_goal_episodes(file, term_states, max_episodes):
    """
    Writes to the file the episode numbers in which
    the goal states were reached
    """
    goal_states_reached = np.nonzero(term_states)[0]
    num_goals = len(goal_states_reached)
    file.write(
        "Number of Times The Agent Reached The Goal: {0}/{1}\n".format(num_goals, max_episodes))
    if num_goals > 0:
        file.write("Episodes Where Goal Was Reached:")
        # Write the episodes where the goal was reached in order to
        # analyse if an optimal path is reached (indicated by episode
        # numbers that are close together consecutively)
        for i in range(num_goals):
            file.write(" {},".format(goal_states_reached[i]))
            if i % 10 == 0 and i != num_goals-1 and i > 0:
                file.write("\n")
                file.write("                                  ")
        file.write("\n")


def write_to_file_results(file, mean_rewards, problem_id, reward_hole, max_episodes, max_iters_per_episode, iters, term_states):
    """
    Writes to the file the results collected from running episodes
    """
    fastest_iters = None
    goal_states_reached = np.nonzero(term_states)[0]
    if len(term_states) > 0:
        fastest_iters = iters[np.argmin(goal_states_reached)]
    file.write("Problem ID:                                {}\n".format(problem_id))
    file.write("Reward Hole:                               {}\n".format(reward_hole))
    file.write("Number of Episodes:                        {}\n".format(max_episodes))
    file.write("Max Number of Iterations per Episode:      {}\n".format(max_iters_per_episode))
    file.write("Max Number of Iterations from Episodes:    {}\n".format(np.max(iters)))
    file.write("Min Number of Iterations from Episodes:    {}\n".format(np.min(iters)))
    file.write("Minimum Number of Steps to Reach the Goal: {}\n".format(fastest_iters or 'N/A'))
    file.write("Covariance of Rewards:                     {}\n".format(np.cov(mean_rewards)))
    file.write("Maximum Mean Reward:                       {}\n".format(np.max(mean_rewards)))
    file.write("Minimum Mean Reward:                       {}\n".format(np.min(mean_rewards)))

