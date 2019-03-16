"""
Helper functions used in the run_simple
"""
from search import (
    PriorityQueue, Node, memoize,
    UndirectedGraph
)


def my_best_first_graph_search(problem, f):
    """
    Taken from Lab 3
    Search the nodes with the lowest f scores first.
    You specify the function f(node) that you want to minimize; for example,
    if f is a heuristic estimate to the goal, then we have greedy best
    first search; if f is node.depth then we have breadth-first search.
    There is a subtlety: the line "f = memoize(f, 'f')" means that the f
    values will be cached on the nodes as they are computed. So after doing
    a best first search you can examine the f values of the path returned.
    """
    # keep a track of the number of iterations for use in evaluation
    iterations = 0
    f = memoize(f, 'f')
    node = Node(problem.initial)
    iterations += 1
    # This is the goal state
    if problem.goal_test(node.state):
        iterations += 1
        return (iterations, node)
    # Create a priority queue that is ordered by its distance
    # from the distance travelled so far (g) + the straight line distance
    # from the new node to the goal state (h)
    frontier = PriorityQueue('min', f)
    frontier.append(node)
    iterations += 1
    explored = set()
    # Loop until there is no more nodes to visit
    while frontier:
        # Get the node with minimum f(n) = g(n) + h(n)
        node = frontier.pop()
        iterations += 1
        # We have reached the goal, return the solution
        if problem.goal_test(node.state):
            iterations += 1
            return iterations
        # Mark the node as visited
        explored.add(node.state)
        # Loop over the nodes neighbours and find the next node
        # with minimum f(n)
        for child in node.expand(problem):
            # Only consider new nodes which havent been explored yet
            # and the ones which we are about to explore in the
            # loop
            if child.state not in explored and child not in frontier:
                frontier.append(child)
                iterations += 1
            # Update the new distance (f(n)) for this node
            # if it is smaller than the previous known one
            elif child in frontier:
                incumbent = frontier[child]
                if f(child) < f(incumbent):
                    del frontier[incumbent]
                    frontier.append(child)
                    iterations += 1
        iterations += 1
    return iterations


def my_astar_search(agent_program, heur=None):
    """
    Taken from Lab 3
    A* search is best-first graph search with f(n) = g(n)+h(n).
    You need to specify the h function when you call astar_search, or
    else in your Problem subclass.
    """
    # define the heuristic function
    heur = memoize(heur or agent_program.problem.h, 'h')
    return my_best_first_graph_search(agent_program.problem, lambda n: n.path_cost + heur(n))


def env2statespace(env):
    """ 
    This simple parser demonstrates how you can extract the state space from the Open AI env

    We *assume* full observability, i.e., we can directly ignore Hole states. Alternatively, 
    we could place a very high step cost to a Hole state or use a directed representation 
    (i.e., you can go to a Hole state but never return). Feel free to experiment with both if time permits.

    Input:
        env: an Open AI Env follwing the std in the FrozenLake-v0 env

    Output:
        state_space_locations : a dict with the available states
        state_space_actions   : a dict of dict with available actions in each state
        state_start_id        : the start state
        state_goal_id         : the goal state  

        These objects are enough to define a Graph problem using the AIMA toolbox, e.g., using  
        UndirectedGraph, GraphProblem and astar_search (as in AI (H) Lab 3)

    Notice: the implementation is very explicit to demonstarte all the steps (it could be made more elegant!)

    """
    state_space_locations = {}  # create a dict
    for i in range(env.desc.shape[0]):
        for j in range(env.desc.shape[1]):
            if not (b'H' in env.desc[i, j]):
                state_id = "S_"+str(int(i))+"_"+str(int(j))
                state_space_locations[state_id] = (int(i), int(j))
                if env.desc[i, j] == b'S':
                    state_initial_id = state_id
                elif env.desc[i, j] == b'G':
                    state_goal_id = state_id

                #-- Generate state / action list --#
                # First define the set of actions in the defined coordinate system
                actions = {"west": [-1, 0], "east": [+1, 0],
                           "north": [0, +1], "south": [0, -1]}
                state_space_actions = {}
                for state_id in state_space_locations:
                    possible_states = {}
                    for action in actions:
                        #-- Check if a specific action is possible --#
                        delta = actions.get(action)
                        state_loc = state_space_locations.get(state_id)
                        state_loc_post_action = [
                            state_loc[0]+delta[0], state_loc[1]+delta[1]]

                        #-- Check if the new possible state is in the state_space, i.e., is accessible --#
                        state_id_post_action = "S_" + \
                            str(state_loc_post_action[0]) + \
                            "_"+str(state_loc_post_action[1])
                        if state_space_locations.get(state_id_post_action) != None:
                            possible_states[state_id_post_action] = 1

                    #-- Add the possible actions for this state to the global dict --#
                    state_space_actions[state_id] = possible_states

    return state_space_locations, state_space_actions, state_initial_id, state_goal_id
