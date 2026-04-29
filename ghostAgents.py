# ghostAgents.py
# --------------
# Informações de Licenciamento: Você é livre para usar ou estender estes projetos para
# fins educacionais, desde que (1) não distribua ou publique soluções,
# (2) mantenha este aviso, e (3) forneça a devida atribuição à UC Berkeley,
# incluindo um link para http://ai.berkeley.edu.
#
# Informações sobre Atribuição: Os projetos de IA do Pacman foram desenvolvidos
# na UC Berkeley. Os projetos principais e autograders foram criados principalmente
# por John DeNero (denero@cs.berkeley.edu) e Dan Klein (klein@cs.berkeley.edu).
# A correção automática do lado do aluno foi adicionada por Brad Miller, Nick Hay e
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


from game import Agent
from game import Actions
from game import Directions
import random
from util import manhattanDistance
import util


class GhostAgent(Agent):
    """
    Classe base para agentes Fantasmas.
    """
    def __init__(self, index):
        self.index = index

    def getAction(self, state):
        """
        Retorna a ação baseada em uma distribuição de probabilidades calculada para o estado.
        """
        dist = self.getDistribution(state)
        if len(dist) == 0:
            return Directions.STOP
        else:
            return util.chooseFromDistribution(dist)

    def getDistribution(self, state):
        """
        Retorna um objeto Counter codificando uma distribuição sobre as ações
        a partir do estado fornecido.
        """
        util.raiseNotDefined()


class RandomGhost(GhostAgent):
    """
    Um fantasma que escolhe uma ação legal de forma uniformemente aleatória.
    (Todas as direções possíveis têm a mesma chance de serem escolhidas).
    """

    def getDistribution(self, state):
        dist = util.Counter()
        for a in state.getLegalActions(self.index):
            dist[a] = 1.0
        dist.normalize()
        return dist


class DirectionalGhost(GhostAgent):
    """
    Um fantasma que prefere perseguir o Pac-Man diretamente, ou fugir quando está assustado.
    """

    def __init__(self, index, prob_attack=0.8, prob_scaredFlee=0.8):
        self.index = index
        self.prob_attack = prob_attack       # Probabilidade de atacar o Pac-Man
        self.prob_scaredFlee = prob_scaredFlee # Probabilidade de fugir se estiver assustado

    def getDistribution(self, state):
        # Lê variáveis importantes do estado atual
        ghostState = state.getGhostState(self.index)
        legalActions = state.getLegalActions(self.index)
        pos = state.getGhostPosition(self.index)
        isScared = ghostState.scaredTimer > 0

        # Define a velocidade (fantasmas andam mais devagar quando assustados)
        speed = 1
        if isScared:
            speed = 0.5

        # Calcula para onde cada ação nos levaria
        actionVectors = [Actions.directionToVector(a, speed) for a in legalActions]
        newPositions = [(pos[0]+a[0], pos[1]+a[1]) for a in actionVectors]
        pacmanPosition = state.getPacmanPosition()

        # Seleciona as melhores ações dado o estado atual
        distancesToPacman = [manhattanDistance(pos, pacmanPosition) for pos in newPositions]
        
        if isScared:
            # Se estiver assustado, o objetivo é maximizar a distância (fugir)
            bestScore = max(distancesToPacman)
            bestProb = self.prob_scaredFlee
        else:
            # Se não estiver assustado, o objetivo é minimizar a distância (atacar)
            bestScore = min(distancesToPacman)
            bestProb = self.prob_attack
            
        # Lista com as ações que levam à melhor pontuação (pode haver empate)
        bestActions = [action for action, distance in zip(legalActions, distancesToPacman) if distance == bestScore]

        # Constrói a distribuição de probabilidades
        dist = util.Counter()
        for a in bestActions:
            # Distribui a "maior probabilidade" entre as melhores ações
            dist[a] = bestProb / len(bestActions)
        for a in legalActions:
            # Distribui a probabilidade restante (1 - bestProb) entre todas as ações legais de forma igual
            dist[a] += (1-bestProb) / len(legalActions)
            
        # Normaliza para garantir que a soma de todas as probabilidades seja 1.0
        dist.normalize()
        return dist
