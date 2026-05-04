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
from pacman import GameState
from multiAgents import MultiAgentSearchAgent


class MinimaxAgent(MultiAgentSearchAgent):
    def getAction(self, gameState: GameState):
        """Seu código vem aqui
        Adicione o código para minimax
        """

        # Garante que a betterEvaluationFunction deste arquivo seja usada
        self.evaluationFunction = betterEvaluationFunction

        def minimax(agentIndex=0, depth=0, state=gameState):
            # verifica se jogo acabou, se sim retorna self.evaluationFunction(state)
            if state.isWin() or state.isLose() or depth == self.depth:
                return self.evaluationFunction(state)

            legalActions = state.getLegalActions(agentIndex)
            if not legalActions:
                return self.evaluationFunction(state)

            # calcula próximo agente
            nextAgent = agentIndex + 1

            # calcula próxima profundidade (apenas quando agentIndex == último fantasma
            # e o próximo agente é o Pac-Man, a profundidade aumenta)
            if nextAgent == state.getNumAgents():
                nextAgent = 0
                nextDepth = depth + 1
            else:
                nextDepth = depth

            # para cada ação possível em state.getLegalActions(agentIndex)
            if agentIndex == 0:  # Passo de maximização (Pac-Man)
                # Remove STOP para evitar que o Pac-Man fique parado no lugar
                legalActions = [a for a in legalActions if a != Directions.STOP]

                maxValue = -float('inf')
                bestAction = None

                for action in legalActions:
                    # calcula o próximo estado com state.generateSuccessor(agentIndex, action)
                    nextState = state.generateSuccessor(agentIndex, action)

                    # calcula o score chamando minimax recursivamente
                    score = minimax(nextAgent, nextDepth, nextState)

                    # se for um passo de maximização e o score for maior que o anterior, selecione ele
                    if score > maxValue:
                        maxValue = score
                        bestAction = action

                # retorne a melhor ação no nível raiz, ou o valor nas chamadas internas
                if depth == 0:
                    return bestAction
                else:
                    return maxValue

            else:  # Passo de minimização (Fantasmas)
                minValue = float('inf')

                for action in legalActions:
                    # calcula o próximo estado com state.generateSuccessor(agentIndex, action)
                    nextState = state.generateSuccessor(agentIndex, action)

                    # calcula o score chamando minimax recursivamente
                    score = minimax(nextAgent, nextDepth, nextState)

                    # se for um passo de minimização e o score for menor que o anterior, selecione ele
                    if score < minValue:
                        minValue = score

                return minValue

        return minimax()


def betterEvaluationFunction(currentGameState: GameState):
    pos = currentGameState.getPacmanPosition()
    food = currentGameState.getFood().asList()
    ghostStates = currentGameState.getGhostStates()

    # Calcula a distância de Manhattan para a comida mais próxima
    foodDistances = [manhattanDistance(pos, f) for f in food]
    if len(foodDistances) > 0:
        minFoodDistance = min(foodDistances)
    else:
        minFoodDistance = 0

    # Distância para o fantasma mais próximo
    ghostDistances = [manhattanDistance(pos, ghost.getPosition()) for ghost in ghostStates]
    minGhostDistance = min(ghostDistances)

    # Aumenta a pontuação se o fantasma estiver assustado, mas penaliza se estiver muito perto
    scaredTimes = [ghostState.scaredTimer for ghostState in ghostStates]
    if min(scaredTimes) > 0:
        minGhostDistance = 0  # Ignora fantasmas assustados

    # + bônus por estar perto da comida (quanto menor a distância, maior o bônus)
    # - penalidade por estar perto de fantasma perigoso
    return currentGameState.getScore() + (1.5 / (minFoodDistance + 1)) - (2 / (minGhostDistance + 1))

# Abbreviation
better = betterEvaluationFunction
