# multiAgents.py
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


from util import manhattanDistance
from game import Directions
import random, util

from game import Agent
from pacman import GameState

class ReflexAgent(Agent):
    """
    Um agente reativo (ReflexAgent) escolhe uma ação em cada ponto de decisão examinando
    suas alternativas por meio de uma função de avaliação de estado.

    O código abaixo é fornecido como um guia. Você é bem-vindo para alterá-lo
    de qualquer forma que achar adequado, contanto que não modifique os cabeçalhos
    dos nossos métodos.
    """


    def getAction(self, gameState: GameState):
        """
        Você não precisa mudar este método, mas fique à vontade para fazê-lo.

        getAction escolhe entre as melhores opções de acordo com a função de avaliação.

        Assim como no projeto anterior, getAction recebe um GameState e retorna
        alguma Directions.X para algum X no conjunto {NORTH, SOUTH, WEST, EAST, STOP}
        """
        # Coleta movimentos legais e os estados sucessores
        legalMoves = gameState.getLegalActions()

        # Escolhe uma das melhores ações
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices) # Escolhe aleatoriamente entre os melhores

        "Adicione mais do seu código aqui, se quiser"

        return legalMoves[chosenIndex]

    def evaluationFunction(self, currentGameState: GameState, action):
        """
        Projete uma função de avaliação melhor aqui.

        A função de avaliação recebe o estado atual e o estado sucessor proposto
        (GameStates em pacman.py) e retorna um número, onde números maiores são melhores.

        O código abaixo extrai algumas informações úteis do estado, como a
        comida restante (newFood) e a posição do Pacman após se mover (newPos).
        newScaredTimes guarda o número de movimentos que cada fantasma permanecerá
        assustado porque o Pacman comeu uma pílula de poder.

        Imprima essas variáveis para ver o que você está recebendo, e então combine-as
        para criar uma função de avaliação magistral.
        """
        # Informações úteis que você pode extrair de um GameState (pacman.py)
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        newPos = successorGameState.getPacmanPosition()
        newFood = successorGameState.getFood()
        newGhostStates = successorGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

        "*** SEU CÓDIGO AQUI ***"
        return successorGameState.getScore()

def scoreEvaluationFunction(currentGameState: GameState):
    """
    Esta função de avaliação padrão simplesmente retorna a pontuação do estado.
    A pontuação é a mesma exibida na interface gráfica do Pacman.

    Esta função de avaliação destina-se ao uso com agentes de busca adversarial
    (não agentes reativos).
    """
    return currentGameState.getScore()

class MultiAgentSearchAgent(Agent):
    """
    Esta classe fornece alguns elementos comuns para todos os seus
    pesquisadores multiagentes. Quaisquer métodos definidos aqui estarão disponíveis
    para o MinimaxPacmanAgent, AlphaBetaPacmanAgent e ExpectimaxPacmanAgent.

    Você *não* precisa fazer nenhuma alteração aqui, mas pode se quiser
    adicionar funcionalidades a todos os seus agentes de busca adversarial. Por favor, não
    remova nada, no entanto.

    Nota: esta é uma classe abstrata: uma que não deve ser instanciada. Ela é
    apenas parcialmente especificada e projetada para ser estendida. Agent (game.py)
    é outra classe abstrata.
    """

    def __init__(self, evalFn = 'scoreEvaluationFunction', depth = '3'):
        self.index = 0 # Pacman é sempre o agente de índice 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)


def betterEvaluationFunction(currentGameState: GameState):
    """
    Função de Avaliação Aprimorada:
    Em vez de olhar apenas para o score do jogo, esta função analisa distâncias 
    em relação a comidas e fantasmas para guiar o Pac-Man de forma mais inteligente.
    """
    pos = currentGameState.getPacmanPosition()       # Posição atual do Pac-Man (coordenadas x, y)
    food = currentGameState.getFood().asList()       # Lista com a posição de todas as comidas restantes no mapa
    ghostStates = currentGameState.getGhostStates()  # Posição e estado de todos os fantasmas

    # 1. Avaliação de Comida
    # Calcula a distância de Manhattan (menor caminho usando grade) para cada comida e encontra a mais próxima
    foodDistances = [manhattanDistance(pos, f) for f in food]
    if len(foodDistances) > 0:
        minFoodDistance = min(foodDistances)
    else:
        minFoodDistance = 0  # Se não houver mais comida, usamos 0 para não dar erro

    # 2. Avaliação de Fantasmas
    # Calcula a distância do fantasma que está mais perto do Pac-Man
    ghostDistances = [manhattanDistance(pos, ghost.getPosition()) for ghost in ghostStates]
    minGhostDistance = min(ghostDistances)

    # Verifica se os fantasmas estão assustados
    scaredTimes = [ghostState.scaredTimer for ghostState in ghostStates]
    
    # Se algum fantasma está assustado, o Pac-Man não precisa fugir dele.
    if min(scaredTimes) > 0:
        minGhostDistance = 0  # Ignoramos a distância do fantasma

    # 3. Fórmula da Pontuação Final
    return currentGameState.getScore() - (1.5 / (minFoodDistance + 1)) + (2 / (minGhostDistance + 1))

# Abreviação da função de avaliação
better = betterEvaluationFunction
