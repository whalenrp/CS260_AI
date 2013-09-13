# search.py
# ---------
# Licensing Information:  You are free to use or extend these projects for 
# educational purposes provided that (1) you do not distribute or publish 
# solutions, (2) you retain this notice, and (3) you provide clear 
# attribution to UC Berkeley, including a link to 
# http://inst.eecs.berkeley.edu/~cs188/pacman/pacman.html
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero 
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and 
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


"""
In search.py, you will implement generic search algorithms which are called
by Pacman agents (in searchAgents.py).
"""

import util

class SearchProblem:
    """
    This class outlines the structure of a search problem, but doesn't implement
    any of the methods (in object-oriented terminology: an abstract class).

    You do not need to change anything in this class, ever.
    """

    def getStartState(self):
        """
        Returns the start state for the search problem
        """
        util.raiseNotDefined()

    def isGoalState(self, state):
        """
          state: Search state

        Returns True if and only if the state is a valid goal state
        """
        util.raiseNotDefined()

    def getSuccessors(self, state):
        """
          state: Search state

        For a given state, this should return a list of triples,
        (successor, action, stepCost), where 'successor' is a
        successor to the current state, 'action' is the action
        required to get there, and 'stepCost' is the incremental
        cost of expanding to that successor
        """
        util.raiseNotDefined()

    def getCostOfActions(self, actions):
        """
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.  The sequence must
        be composed of legal moves
        """
        util.raiseNotDefined()


def tinyMazeSearch(problem):
    """
    Returns a sequence of moves that solves tinyMaze.  For any other
    maze, the sequence of moves will be incorrect, so only use this for tinyMaze
    """
    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    return  [s,s,w,s,w,w,s,w]

def top(list):
    """
    Utility function for returning the last element in a list.
    """ 
    return list[len(list)-1]

def depthFirstSearch(problem):
    """
    Search the deepest nodes in the search tree first

    Your search algorithm needs to return a list of actions that reaches
    the goal.  Make sure to implement a graph search algorithm

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:

    print "Start:", problem.getStartState()
    print "Is the start a goal?", problem.isGoalState(problem.getStartState())
    print "Start's successors:", problem.getSuccessors(problem.getStartState())
    """

    # Initialize variables
    visited = set([]) # List of visited positions

    def recurse(state):
        """
        This function returns a tuple of a list of directions
        to the goal state from the current state and a boolean
        indicating success or failure
        (True, [path,to,goal])
        """
        if problem.isGoalState(state):
            return (True,[])
        visited.add(state)
        for edge in problem.getSuccessors(state):
            if edge[0] not in visited:
                path = recurse(edge[0])
                if path[0]:
                    return (True,[edge[1]] + path[1])
        return (False,[])
        

    return recurse(problem.getStartState())[1]


class Node:
    """
    Node class for containing a given state and the path from the start state 
    to this state.
    Each state has attached to it the position and path
    """
    def __init__(self,state,path,cost=0):
        self.mState = state
        self.mPath = path
        self.mCost = cost


def breadthFirstSearch(problem):
    """
    Search the shallowest nodes in the search tree first.
    """

    # Initialize variables
    fringeQueue = util.Queue()
    node = Node(problem.getStartState(),[])
    fringeQueue.push(node)
    visited = set([]) # List of visited positions

    while not fringeQueue.isEmpty():
        curState = fringeQueue.pop()
        visited.add(curState.mState);
        if problem.isGoalState(curState.mState):
            return curState.mPath
        for edge in problem.getSuccessors(curState.mState):
            if edge[0] not in visited:
                newState = Node(edge[0],curState.mPath + [edge[1]])
                fringeQueue.push(newState)
                visited.add(edge[0])


def uniformCostSearch(problem):
    "Search the node of least total cost first. "
    # Initialize variables
    fringeQueue = util.PriorityQueue()
    node = Node(problem.getStartState(),[])
    fringeQueue.push(node,0)
    visited = dict([]) # List of visited positions
    visited[problem.getStartState()] = 0

    while not fringeQueue.isEmpty():
        curState = fringeQueue.pop()
        # While this path is not our cheapest path to this node,
        while curState.mCost > visited[curState.mState] :
            # Discard it and move on.
            curState = fringeQueue.pop()

        if problem.isGoalState(curState.mState):
            return curState.mPath
        for edge in problem.getSuccessors(curState.mState):
            newState = Node(edge[0],curState.mPath + [edge[1]], curState.mCost + edge[2])
            if edge[0] not in visited:
                visited[edge[0]] = newState.mCost
            elif newState.mCost < visited[edge[0]]:
                visited[edge[0]] = newState.mCost
            fringeQueue.push(newState,newState.mCost)

def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem, heuristic=nullHeuristic):
    "Search the node that has the lowest combined cost and heuristic first."
    "*** YOUR CODE HERE ***"

    # Initialize variables
    fringeQueue = util.PriorityQueue()
    node = Node(problem.getStartState(),[],0)
    fringeQueue.push(node, heuristic(problem.getStartState(),problem))
    visited = dict([]) # List of visited positions
    visited[problem.getStartState()] = node.mCost

    while not fringeQueue.isEmpty():
        curState = fringeQueue.pop()
        # While this path is not our cheapest path to this node,
        while curState.mCost > visited[curState.mState] :
            # Discard it and move on.
            curState = fringeQueue.pop()

        if problem.isGoalState(curState.mState):
            return curState.mPath
        for edge in problem.getSuccessors(curState.mState):
            newState = Node(edge[0], curState.mPath + [edge[1]], curState.mCost + edge[2])
            if edge[0] not in visited:
                visited[edge[0]] = newState.mCost
            elif newState.mCost < visited[edge[0]]:
                visited[edge[0]] = newState.mCost
            fringeQueue.push(newState,newState.mCost + heuristic(edge[0], problem))

# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
