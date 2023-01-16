# multiAgents.py
# --------------
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


from util import manhattanDistance
from game import Directions
import random, util

from game import Agent


class ReflexAgent(Agent):
    """
    A reflex agent chooses an action at each choice point by examining
    its alternatives via a state evaluation function.

    The code below is provided as a guide.  You are welcome to change
    it in any way you see fit, so long as you don't touch our method
    headers.
    """

    def getAction(self, gameState):
        """
        You do not need to change this method, but you're welcome to.

        getAction chooses among the best options according to the evaluation function.

        Just like in the previous project, getAction takes a GameState and returns
        some Directions.X for some X in the set {NORTH, SOUTH, WEST, EAST, STOP}
        """
        # Collect legal moves and successor states
        legalMoves = gameState.getLegalActions()

        # Choose one of the best actions
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices)  # Pick randomly among the best

        "Add more of your code here if you want to"

        return legalMoves[chosenIndex]

    def evaluationFunction(self, currentGameState, action):
        """
        Design a better evaluation function here.

        The evaluation function takes in the current and proposed successor
        GameStates (pacman.py) and returns a number, where higher numbers are better.

        The code below extracts some useful information from the state, like the
        remaining food (newFood) and Pacman position after moving (newPos).
        newScaredTimes holds the number of moves that each ghost will remain
        scared because of Pacman having eaten a power pellet.

        Print out these variables to see what you're getting, then combine them
        to create a masterful evaluation function.
        """
        # Useful information you can extract from a GameState (pacman.py)
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        newPos = successorGameState.getPacmanPosition()
        newFood = successorGameState.getFood()
        newGhostStates = successorGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

        "*** YOUR CODE HERE ***"
        FoodsList=newFood.asList()
        GhostPosition=successorGameState.getGhostPositions()                        
        FoodDistance=[]                                                        
        GhostDistance=[]

        for Food in FoodsList:
            FoodDistance.append(manhattanDistance(Food,newPos))
        for Ghost in GhostPosition:
            GhostDistance.append(manhattanDistance(Ghost,newPos))

       

        for distance in GhostDistance:                             
            if distance<2:
                return (-(float("inf")))
        if len(FoodDistance)==0:
            return float("inf")
        if currentGameState.getPacmanPosition()==newPos:
            return(-(float("inf")))                                               
        return 10000/sum(FoodDistance) +100000/len(FoodsList)


def scoreEvaluationFunction(currentGameState):
    """
    This default evaluation function just returns the score of the state.
    The score is the same one displayed in the Pacman GUI.

    This evaluation function is meant for use with adversarial search agents
    (not reflex agents).
    """
    return currentGameState.getScore()


class MultiAgentSearchAgent(Agent):
    """
    This class provides some common elements to all of your
    multi-agent searchers.  Any methods defined here will be available
    to the MinimaxPacmanAgent, AlphaBetaPacmanAgent & ExpectimaxPacmanAgent.

    You *do not* need to make any changes here, but you can if you want to
    add functionality to all your adversarial search agents.  Please do not
    remove anything, however.

    Note: this is an abstract class: one that should not be instantiated.  It's
    only partially specified, and designed to be extended.  Agent (game.py)
    is another abstract class.
    """

    def __init__(self, evalFn='scoreEvaluationFunction', depth='2'):
        self.index = 0  # Pacman is always agent index 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)


class MinimaxAgent(MultiAgentSearchAgent):
    """
    Your minimax agent (question 2)
    """

    def getAction(self, gameState):
        """
        Returns the minimax action from the current gameState using self.depth
        and self.evaluationFunction.

        Here are some method calls that might be useful when implementing minimax.

        gameState.getLegalActions(agentIndex):
        Returns a list of legal actions for an agent
        agentIndex=0 means Pacman, ghosts are >= 1

        gameState.generateSuccessor(agentIndex, action):
        Returns the successor game state after an agent takes an action

        gameState.getNumAgents():
        Returns the total number of agents in the game

        gameState.isWin():
        Returns whether or not the game state is a winning state

        gameState.isLose():
        Returns whether or not the game state is a losing state
        """
        "*** YOUR CODE HERE ***"
        def MaxValue(gameState,depth):
            vmax=-(float("inf")) 
            Action=None
            allActions=gameState.getLegalActions(0)
            if len(allActions)==0 or gameState.isWin() or gameState.isLose() or depth==self.depth:             
                return(self.evaluationFunction(gameState),None)
            for action in allActions:                                                  
                successorVal=MinValue(gameState.generateSuccessor(0,action),1,depth)                          
                successorVal=successorVal[0]                                     
                if(successorVal>vmax):                                                
                    vmax,Action=successorVal,action
            return(vmax,Action)

        def MinValue(gameState,agentID,depth):
            vmin=float("inf")
            Action=None
            allActions=gameState.getLegalActions(agentID)
            if len(allActions) == 0:
                return(self.evaluationFunction(gameState),None)
            for action in allActions:
                if(agentID==gameState.getNumAgents()-1):
                    successorVal=MaxValue(gameState.generateSuccessor(agentID,action),depth+1)
                else:
                    successorVal=MinValue(gameState.generateSuccessor(agentID,action),agentID+1,depth)
                successorVal=successorVal[0]
                if(successorVal<vmin):
                    vmin,Action=successorVal,action
            return(vmin,Action)
        return MaxValue(gameState,0)[1]

class AlphaBetaAgent(MultiAgentSearchAgent):
    """
    Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
        Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        a=-(float("inf"))
        b=float("inf")
        def MaxValue(gameState,depth,a,b):
            vmax=-(float("inf")) 
            Action=None
            allActions=gameState.getLegalActions(0)
            if len(allActions)==0 or gameState.isWin() or gameState.isLose() or depth==self.depth:             
                return(self.evaluationFunction(gameState),None)
            for action in allActions:                                                  
                successorVal=MinValue(gameState.generateSuccessor(0,action),1,depth,a,b)                          
                successorVal=successorVal[0]                                     
                if(successorVal>vmax):                                                
                    vmax,Action=successorVal,action
                if vmax>b:
                    return (vmax,Action)
                a=max(a,vmax)
            return(vmax,Action)

        def MinValue(gameState,agentID,depth,a,b):
            vmin=float("inf")
            Action=None
            allActions=gameState.getLegalActions(agentID)
            if len(allActions) == 0:
                return(self.evaluationFunction(gameState),None)
            for action in allActions:
                if(agentID==gameState.getNumAgents()-1):
                    successorVal=MaxValue(gameState.generateSuccessor(agentID,action),depth+1,a,b)
                else:
                    successorVal=MinValue(gameState.generateSuccessor(agentID,action),agentID+1,depth,a,b)
                successorVal=successorVal[0]
                if(successorVal<vmin):
                    vmin,Action=successorVal,action
                if (vmin<a):
                    return (vmin,Action)
                b=min(b,vmin)
            return(vmin,Action)
        return MaxValue(gameState,0,a,b)[1]

class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """

    def getAction(self, gameState):
        """
        Returns the expectimax action using self.depth and self.evaluationFunction

        All ghosts should be modeled as choosing uniformly at random from their
        legal moves.
        """
        "*** YOUR CODE HERE ***"
        def MaxValue(gameState,depth):
            vmax=-(float("inf")) 
            Action=None
            allActions=gameState.getLegalActions(0)
            if len(allActions)==0 or gameState.isWin() or gameState.isLose() or depth==self.depth:             
                return(self.evaluationFunction(gameState),None)
            for action in allActions:                                                  
                successorVal=ExpValue(gameState.generateSuccessor(0,action),1,depth)                          
                successorVal=successorVal[0]                                     
                if(successorVal>vmax):                                                
                    vmax,Action=successorVal,action
            return(vmax,Action)

        def ExpValue(gameState,agentID,depth):
            vexp=0
            Action=None
            allActions=gameState.getLegalActions(agentID)
            if len(allActions) == 0:
                return(self.evaluationFunction(gameState),None)
            for action in allActions:
                if(agentID==gameState.getNumAgents()-1):
                    successorVal=MaxValue(gameState.generateSuccessor(agentID,action),depth+1)
                else:
                    successorVal=ExpValue(gameState.generateSuccessor(agentID,action),agentID+1,depth)
                successorVal=successorVal[0]
                probability=successorVal/len(allActions)
                vexp+=probability
            return(vexp,Action)
        return MaxValue(gameState,0)[1]


def betterEvaluationFunction(currentGameState):
    """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
    evaluation function (question 5).

    DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"
    pacmanPosition=currentGameState.getPacmanPosition()
    ghostsList=currentGameState.getGhostStates()
    Food=currentGameState.getFood()
    Capsules=currentGameState.getCapsules()
    if currentGameState.isWin():
        return float("inf")
    if currentGameState.isLose():
        return float("-inf")
    FoodDistList=[]
    GhostDistList=[]
    ScGhostDistList=[]
    for food in Food.asList():
        FoodDistList+=[util.manhattanDistance(food,pacmanPosition)]
    minFoodDist=min(FoodDistList)
    for ghost in ghostsList:
        if ghost.scaredTimer==0:
            GhostDistList+=[util.manhattanDistance(pacmanPosition,ghost.getPosition())]
        elif ghost.scaredTimer>0:
            ScGhostDistList+=[util.manhattanDistance(pacmanPosition,ghost.getPosition())]
    minGhostDist=-1
    if len(GhostDistList) > 0:
        minGhostDist=min(GhostDistList)
    minScrdGhostDist=-1
    if len(ScGhostDistList)>0:
        minScrdGhostDist=min(ScGhostDistList)
    oldScore=scoreEvaluationFunction(currentGameState)
    BetterScore=oldScore-(2 * minFoodDist + 3 * (1.0/minGhostDist) + 2.5 * minScrdGhostDist + 15 * len(Capsules) + 5 * len(Food.asList()))
    return BetterScore


# Abbreviation
better = betterEvaluationFunction
