"""
Script which defines the SimpleAgent class which uses informed search methods
(A* search) in this case to solve the LochLomondEnv problem
"""
import sys
import time
from pprint import pprint
from math import sqrt
import numpy as np
from uofgsocsai import LochLomondEnv
from helpers import env2statespace
from constants import ( 
    MAX_EPISODES, MAX_ITERS_PER_EPISODE, REWARD_HOLE
)
from search import ( 
    GraphProblem, PriorityQueue, Node, memoize,
    UndirectedGraph
)

# Read in problem ID ad command line argument, and provide default if
# one wasnt provided
if len(sys.argv) == 2:
    PROBLEM_ID = int(sys.argv[1])
else:
    PROBLEM_ID = 0


class SimpleAgent:
    """
    Class to represent a Simple Agent that uses A* search in
    order to solve the LochLomondEnv problem
    """

    def __init__(self, problem_id):
        """
        Constructor to initialise the environment for the simple agent
        """
        self.env = LochLomondEnv(problem_id=problem_id,
                                 is_stochastic=False,
                                 reward_hole=0.0)
        w, x, y, z = env2statespace(self.env)
        self.state_space_locations = w
        self.state_space_actions = x
        self.state_initial_id = y
        self.state_goal_id = z
        self.map = UndirectedGraph(self.state_space_actions)
        self.problem = GraphProblem('{0}'.format(self.state_initial_id), '{0}'.format(self.state_goal_id), self.map)

    def __my_best_first_graph_search(self, problem, f):
        """Search the nodes with the lowest f scores first.
        You specify the function f(node) that you want to minimize; for example,
        if f is a heuristic estimate to the goal, then we have greedy best
        first search; if f is node.depth then we have breadth-first search.
        There is a subtlety: the line "f = memoize(f, 'f')" means that the f
        values will be cached on the nodes as they are computed. So after doing
        a best first search you can examine the f values of the path returned."""
        print("Initial state: " + self.state_initial_id)
        print("Initial state: " + self.state_goal_id)
        # we use these two variables at the time of visualisations
        iterations = 0
        f = memoize(f, 'f')
        node = Node(self.problem.initial)
        iterations += 1
        if self.problem.goal_test(node.state):
            iterations += 1
            return(iterations, node)
        frontier = PriorityQueue('min', f)
        frontier.append(node)
        iterations += 1
        explored = set()
        while frontier:
            node = frontier.pop()
            iterations += 1
            if self.problem.goal_test(node.state):
                iterations += 1
                return(iterations, node)
            explored.add(node.state)
            for child in node.expand(self.problem):
                if child.state not in explored and child not in frontier:
                    frontier.append(child)
                    iterations += 1
                elif child in frontier:
                    incumbent = frontier[child]
                    if f(child) < f(incumbent):
                        del frontier[incumbent]
                        frontier.append(child)
                        iterations += 1
            iterations += 1
    
    def my_astar_search(self, h=None):
        """A* search is best-first graph search with f(n) = g(n)+h(n).
        You need to specify the h function when you call astar_search, or
        else in your Problem subclass."""
        h = memoize(h or self.problem.h, 'h') # define the heuristic function
        return self.__my_best_first_graph_search(self.problem, lambda n: n.path_cost + h(n))

simple_agent = SimpleAgent(0)
pprint(simple_agent.my_astar_search(h=None))