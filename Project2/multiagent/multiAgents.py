# multiAgents.py
# --------------
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
        some Directions.X for some X in the set {North, South, West, East, Stop}
        """
        # Collect legal moves and successor states
        legalMoves = gameState.getLegalActions()

        # Choose one of the best actions
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices) # Pick randomly among the best

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

        # First check to see if we eat a pellet by coming to this state.
        score = 0
        if len(newFood.asList()) < len(currentGameState.getFood().asList()):
            score = 10000

        # Find the closest food pellet and take the inverse of its 
        # manhattan distance.
        minManhattanDist = 9999999;
        for food in newFood.asList():
            manhat = util.manhattanDistance(newPos, food)
            if manhat < minManhattanDist:
                minManhattanDist = manhat

        score += (1.0/minManhattanDist)

        # Make the state undesirable if it is a ghost's state.
        for ghostState in newGhostStates:
            curGhostDist = util.manhattanDistance(ghostState.getPosition(), newPos)
            if curGhostDist < 2:
                score *= (-20000)
            
        if currentGameState == successorGameState:
            return -1000
        else:
            return score
        #return successorGameState.getScore()

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

    def __init__(self, evalFn = 'scoreEvaluationFunction', depth = '2'):
        self.index = 0 # Pacman is always agent index 0
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
        """
        "*** YOUR CODE HERE ***"
        numAgents = gameState.getNumAgents()

        def maxState(state, depth):
            """
            Returns a tuple containing a value and the associated action as determined
            by the maximum of possible actions for the given state.
            """
            agentIndex = depth % numAgents
            actions = state.getLegalActions(agentIndex);

            if depth < 1 or state.isLose() or state.isWin():
               return (self.evaluationFunction(state), Directions.STOP)

            if len(actions) is 0:
                return minState(state.generateSuccessor(agentIndex,Directions.STOP),depth-1)
        
            maxPair = (-999999,Directions.STOP)
            for action in actions:
                
                nextState = minState(state.generateSuccessor(agentIndex,action),depth-1)
                if maxPair[0] < nextState[0]:
                    maxPair = (nextState[0],action)
                    
            return maxPair

        def minState(state, depth):
            """
            Returns a tuple containing a value and the associated action as determined
            by the minimum of possible actions for the given state.
            """
            agentIndex = depth % numAgents
            actions = state.getLegalActions(agentIndex)
            
            if depth < 1 or state.isLose() or state.isWin():
                return (self.evaluationFunction(state), Directions.STOP)

            if len(actions) is 0:
                # If our next node is not pacman
                if (agentIndex - 1) is not 0:
                    return minState(state.generateSuccessor(agentIndex,Directions.STOP),depth-1)
                else:
                    return maxState(state.generateSuccessor(agentIndex,Directions.STOP),depth-1)
                    

            minPair = (999998,Directions.STOP)
            for action in actions:
                # If our next node is not pacman
                if (agentIndex - 1) is not 0:
                    nextPair = minState(state.generateSuccessor(agentIndex,action),depth-1)
                else:
                    nextPair = maxState(state.generateSuccessor(agentIndex,action),depth-1)

                if minPair[0] > nextPair[0]:
                    minPair = (nextPair[0],action)
            return minPair
            

        return maxState(gameState,self.depth*numAgents)[1]

class AlphaBetaAgent(MultiAgentSearchAgent):
    """
      Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
          Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        util.raiseNotDefined()

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
        util.raiseNotDefined()

def betterEvaluationFunction(currentGameState):
    """
      Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
      evaluation function (question 5).

      DESCRIPTION: (currentScore + 1/#pellets + 1/(sum_of_manhattan_to_pellets)) - whether or not a ghost is nearby
    """
    # Get #pellets
    pellets = currentGameState.getFood()
    numPellets = len(pellets)
    
    # Get sum of manhattan distances
    currentPos = currentGameState.getPacmanPosition()
    sumManhattan = 0
    for pellet in pellets:
        sumManhattan += util.manhattanDistance(currentPos, pellet)
        
    # Process ghost positions
    score = 1
    for ghostState in newGhostStates:
        curGhostDist = util.manhattanDistance(ghostState.getPosition(), newPos)
        if curGhostDist < 2:
            score *= (-1)
            break
            
    return (currentGameState.getScore() + (1.0)/numPellets + 1.0/(sumManhattan))- (score*1000)
                
    #return currentGameState.getScore()

# Abbreviation
better = betterEvaluationFunction

class ContestAgent(MultiAgentSearchAgent):
    """
      Your agent for the mini-contest
    """

    def getAction(self, gameState):
        """
          Returns an action.  You can use any method you want and search to any depth you want.
          Just remember that the mini-contest is timed, so you have to trade off speed and computation.

          Ghosts don't behave randomly anymore, but they aren't perfect either -- they'll usually
          just make a beeline straight towards Pacman (or away from him if they're scared!)
        """
        "*** YOUR CODE HERE ***"
        util.raiseNotDefined()

