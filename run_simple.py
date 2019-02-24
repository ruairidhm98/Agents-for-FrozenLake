"""
Script which defines the SimpleAgent class which uses informed search methods
(A* search) in this case to solve the LochLomondEnv problem
"""
import sys
import time
from math import sqrt
import numpy as np
from constants import *
from pprint import pprint
from agent import Agent
from uofgsocsai import LochLomondEnv
from utils import PriorityQueue, memoize
from search import GraphProblem, Node, astar_search, best_first_graph_search, UndirectedGraph


if len(sys.argv) == 2: 
    PROBLEM_ID = int(sys.argv[1])
else: 
    PROBLEM_ID = 0

def astar_search(graph, initial, goal, heuristics):
    
    iterations = 0
    pqueue = PriorityQueue('min')
    if initial == goal:
        iterations += 1
        return (iterations)

def my_best_first_graph_search(problem, f):
    """Search the nodes with the lowest f scores first.
    You specify the function f(node) that you want to minimize; for example,
    if f is a heuristic estimate to the goal, then we have greedy best
    first search; if f is node.depth then we have breadth-first search.
    There is a subtlety: the line "f = memoize(f, 'f')" means that the f
    values will be cached on the nodes as they are computed. So after doing
    a best first search you can examine the f values of the path returned."""
    
    # we use these two variables at the time of visualisations
    iterations = 0
    all_node_colors = []

    f = memoize(f, 'f')
    node = Node(problem.initial)  
    iterations += 1
    all_node_colors.append(dict(node_colors))
    if problem.goal_test(node.state):
        iterations += 1
        all_node_colors.append(dict(node_colors))
        return(iterations, all_node_colors, node)
    frontier = PriorityQueue('min', f)
    frontier.append(node)
    iterations += 1
    all_node_colors.append(dict(node_colors))
    explored = set()
    while frontier:
        node = frontier.pop()
        iterations += 1
        all_node_colors.append(dict(node_colors))
        if problem.goal_test(node.state):
            iterations += 1
            all_node_colors.append(dict(node_colors))
            return(iterations, all_node_colors, node)
        explored.add(node.state)
        for child in node.expand(problem):
            if child.state not in explored and child not in frontier:
                frontier.append(child)
                iterations += 1
                all_node_colors.append(dict(node_colors))
            elif child in frontier:
                incumbent = frontier[child]
                if f(child) < f(incumbent):
                    del frontier[incumbent]
                    frontier.append(child)
                    iterations += 1
                    all_node_colors.append(dict(node_colors))
        iterations += 1
        all_node_colors.append(dict(node_colors))


class SimpleAgent(Agent):
    """
    Class to represent a Simple Agent that uses A* search in
    order to solve the LochLomondEnv problem
    """
    def create_problem():
        """
        Creates the problem for the agent to solve
        """
        goal_state = np.where(self.env.desc == b'G')
        goal_x = goal_state[0][0]
        goal_y = goal_state[1][0]        
        problem = GraphProblem("S", "G", self.env.desc)

    def __solve(self, max_episodes, max_iters_per_episode, reward_hole):
        """
        Solves the search problem using A* search, returns
        the rewards collected and the time taken in each 
        iteration
        """
        pass

    def __generate_heuristics(self):
        """
        Generates the heuristic function h(n) used in the A* search algorithm,
        the heuristic being the Euclidean distance from the current node
        to the goal node. Returns a dictionary representing the value of
        h(n) for each position (i,j) in the graph
        """
        shape = self.env.desc.shape
        heuristics = np.zeros(shape, dtype=np.float64)
        goal_state = np.where(self.env.desc == b'G')
        goal_x = goal_state[0][0]
        goal_y = goal_state[1][0]
        rows = shape[0]
        cols = shape[1]
        # Use the Euclidean distance to compute the distance to the
        # goal node
        for i in range(rows):
            for j in range(cols):
                heuristics[i,j] = sqrt((i - goal_x)**2 + (j - goal_y)**2)
        return heuristics

    def solve_and_display(self, max_episodes, max_iter_per_episode, reward_hole):
        """
        Collects, then displays the results
        """
        pass


simple_agent = SimpleAgent(PROBLEM_ID, False, REWARD_HOLE)
