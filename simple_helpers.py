"""
Helper functions used in the simple agent
"""
from math import sqrt
import numpy as np

def generate_heuristics(env):
    """
    Generates the heuristic function h(n) used in the A* search algorithm,
    the heuristic being the Euclidean distance from the current node
    to the goal node. Returns a dictionary representing the value of
    h(n) for each position (i,j) in the graph
    """
    shape = env.desc.shape
    heuristics = np.zeros(shape, dtype=np.float64)
    goal_state = np.where(env.desc == b'G')
    goal_x = goal_state[0][0]
    goal_y = goal_state[1][0]
    rows = shape[0]
    cols = shape[1]
    # Use the Euclidean distance to compute the distance to the
    # goal node
    for i in range(rows):
        for j in range(cols):
            heuristics[i, j] = sqrt((i - goal_x)**2 + (j - goal_y)**2)

    return heuristics
