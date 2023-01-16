# search.py
# ---------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


"""
In search.py, you will implement generic search algorithms which are called by
Pacman agents (in searchAgents.py).
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
        Returns the start state for the search problem.
        """
        util.raiseNotDefined()

    def isGoalState(self, state):
        """
          state: Search state

        Returns True if and only if the state is a valid goal state.
        """
        util.raiseNotDefined()

    def getSuccessors(self, state):
        """
          state: Search state

        For a given state, this should return a list of triples, (successor,
        action, stepCost), where 'successor' is a successor to the current
        state, 'action' is the action required to get there, and 'stepCost' is
        the incremental cost of expanding to that successor.
        """
        util.raiseNotDefined()

    def getCostOfActions(self, actions):
        """
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.
        The sequence must be composed of legal moves.
        """
        util.raiseNotDefined()


def tinyMazeSearch(problem):
    """
    Returns a sequence of moves that solves tinyMaze.  For any other maze, the
    sequence of moves will be incorrect, so only use this for tinyMaze.
    """
    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    return  [s, s, w, s, w, w, s, w]

def depthFirstSearch(problem):
    """
    Search the deepest nodes in the search tree first.

    Your search algorithm needs to return a list of actions that reaches the
    goal. Make sure to implement a graph search algorithm.

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:

    print("Start:", problem.getStartState())
    print("Is the start a goal?", problem.isGoalState(problem.getStartState()))
    print("Start's successors:", problem.getSuccessors(problem.getStartState()))
    """
    "*** YOUR CODE HERE ***"

    fring = util.Stack()
    startingState = problem.getStartState()
    if problem.isGoalState(startingState):
        return []

    
    expNodes = []
    # startNode(node,actions)
    startNode = (startingState, [])
    fring.push(startNode)

    while fring.isEmpty()==False:
        curntState, actions = fring.pop()
        if curntState not in expNodes:
            expNodes.append(curntState)

            if problem.isGoalState(curntState):
                return actions
            else:
                successors = problem.getSuccessors(curntState)

            for nextNode, action, cost in successors:
                newAction = actions + [action]
                fring.push((nextNode, newAction))
                
def breadthFirstSearch(problem):
    """Search the shallowest nodes in the search tree first."""
    "*** YOUR CODE HERE ***"
    
    fring = util.Queue()
    startingState = problem.getStartState()
    if problem.isGoalState(startingState):
        return []

    
    expNodes = []
    # startNode(node,actions)
    startNode = (startingState, [])
    fring.push(startNode)

    while fring.isEmpty()==False:
        curntState, actions = fring.pop()
        if curntState not in expNodes:
            expNodes.append(curntState)

            if problem.isGoalState(curntState):
                return actions
            else:
                successors = problem.getSuccessors(curntState)

            for nextNode, action, cost in successors:
                newAction = actions + [action]
                fring.push((nextNode, newAction))
                
def uniformCostSearch(problem):
    """Search the node of least total cost first."""
    "*** YOUR CODE HERE ***"

    fring = util.PriorityQueue()

    expNodes = {}
    
    startingState = problem.getStartState()
    
    #(state, action, cost)
    startingNode = (startingState, [], 0) 
    fring.push(startingNode, 0)
    
    while  fring.isEmpty()==False:
        curntState, actions, curntCost = fring.pop()
       
        if (curntState not in expNodes) or (curntCost < expNodes[curntState]):
            expNodes[curntState] = curntCost
            if problem.isGoalState(curntState):
                return actions
            else:
                # (successor, action, stepCost)
                successors = problem.getSuccessors(curntState)
            
                for succState, succAction, succCost in successors:
                    NewAction = actions + [succAction]
                    NewCost = curntCost + succCost
                    NewNode = (succState, NewAction, NewCost)
                    fring.update(NewNode, NewCost)

    return actions
    
def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    "*** YOUR CODE HERE ***"

    
    fring = util.PriorityQueue()
    expNodes = [] #(state, cost)
    startingState = problem.getStartState()
    
    #(state, action, cost)
    startingNode = (startingState, [], 0) 
    fring.push(startingNode, 0)

    while fring.isEmpty()==False:

        curntState, actions, curntCost = fring.pop()
        expNodes.append((curntState, curntCost))
        if problem.isGoalState(curntState):
            return actions

        else:
            #(successor, action, stepCost)
            successors = problem.getSuccessors(curntState)

            for sucState, sucAction, sucCost in successors:
                NewAction = actions + [sucAction]
                NewCost = problem.getCostOfActions(NewAction)
                NewNode = (sucState, NewAction, NewCost)
                already_explored = False
                for Explored in expNodes:
                    expState, expCost = Explored
                    if (sucState == expState) and (NewCost >= expCost):
                        already_explored = True

                if already_explored==False:
                    fring.push(NewNode, NewCost + heuristic(sucState, problem))
                    expNodes.append((sucState, NewCost))

    return actions

# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
