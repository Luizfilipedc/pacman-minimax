# seuPacManAgents.py
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
from multiAgents import MultiAgentSearchAgent


class MinimaxAgent(MultiAgentSearchAgent):
    """
    Seu agente Minimax (projeto 2)
    Esta classe estende MultiAgentSearchAgent, de onde herda self.depth (profundidade
    limite da árvore de busca) e self.evaluationFunction (função de avaliação do estado).
    """

    def getAction(self, gameState: GameState):
        """
        Retorna a ação do minimax a partir do gameState (estado atual do jogo).
        
        O Pac-Man é sempre o agente 0, e os fantasmas são os agentes 1, 2, etc.
        Portanto, o agente 0 deve tentar MAXIMIZAR sua pontuação, enquanto os
        agentes fantasmas tentarão MINIMIZAR a pontuação do Pac-Man.
        """

        def minimax(agentIndex=0, depth=0, state=gameState):
            """
            Função recursiva principal do Minimax.
            
            Parâmetros:
            - agentIndex: Inteiro que indica de quem é a vez (0 para Pac-Man, > 0 para fantasmas).
            - depth: Profundidade atual na árvore de busca.
            - state: O estado do jogo a ser avaliado.
            
            Retorno:
            - Uma tupla (melhor_valor, melhor_acao).
            """
            # 1. Condição de Parada
            # A recursão para se o jogo for ganho ou perdido, ou se chegarmos na profundidade máxima estabelecida.
            if state.isWin() or state.isLose() or depth == self.depth:
                return self.evaluationFunction(state), None

            # Obtém todas as ações permitidas para o agente atual no momento
            legalActions = state.getLegalActions(agentIndex)
            
            # Remove a ação de ficar parado (Stop) para o Pac-Man. 
            # Isso evita o problema de 'thrashing', onde o Pac-Man fica num loop infinito
            # se movendo de um lado para o outro por causa de pontuações empatadas e não pega a comida.
            if agentIndex == 0 and Directions.STOP in legalActions:
                legalActions.remove(Directions.STOP)

            # Se por acaso o agente não tiver mais nenhuma ação disponível, retorna o valor do estado
            if not legalActions:
                return self.evaluationFunction(state), None

            # 2. Transição de Agente e Profundidade
            # Verifica a quantidade total de agentes no jogo (1 Pac-Man + N Fantasmas)
            numAgents = state.getNumAgents()
            
            # O próximo agente é o agente atual + 1. Se ultrapassar o total de agentes, volta para o 0 (Pac-Man)
            nextAgent = (agentIndex + 1) % numAgents
            
            # A profundidade da árvore só aumenta quando o "turno" completo termina, 
            # ou seja, quando a vez volta para o Pac-Man (nextAgent == 0)
            nextDepth = depth + 1 if nextAgent == 0 else depth

            # 3. Lógica do Nó MAX (Pac-Man)
            if agentIndex == 0:
                bestValue = float('-inf')  # Começa com o menor valor possível (menos infinito)
                bestActions = []           # Lista para guardar empates e ajudar no desempate aleatório

                for action in legalActions:
                    # Gera como o jogo ficaria se o Pac-Man tomasse essa 'action'
                    successor = state.generateSuccessor(agentIndex, action)
                    
                    # Chama o minimax recursivamente para o próximo agente avaliar este sucessor
                    value, _ = minimax(nextAgent, nextDepth, successor)
                    
                    # Se encontrou um valor maior, este se torna o nosso novo 'bestValue'
                    if value > bestValue:
                        bestValue = value
                        bestActions = [action]       # Reinicia a lista de melhores ações
                    
                    # Se o valor for igual ao melhor já encontrado, é um empate
                    elif value == bestValue:
                        bestActions.append(action)   # Adiciona a ação empatada na lista
                
                # Escolhe aleatoriamente uma das melhores ações empatadas
                # (ajuda o Pac-Man a explorar o mapa caso várias direções tenham notas idênticas)
                bestAction = random.choice(bestActions) if bestActions else None
                return bestValue, bestAction

            # 4. Lógica do Nó MIN (Fantasmas)
            else:
                bestValue = float('inf')   # Começa com o maior valor possível (mais infinito)
                bestAction = None

                for action in legalActions:
                    # Gera como o jogo ficaria se o Fantasma tomasse essa 'action'
                    successor = state.generateSuccessor(agentIndex, action)
                    
                    # Chama o minimax recursivamente para simular os próximos turnos da árvore
                    value, _ = minimax(nextAgent, nextDepth, successor)
                    
                    # O Fantasma quer MINIMIZAR o valor do Pac-Man, então busca o MENOR valor
                    if value < bestValue:
                        bestValue = value
                        bestAction = action
                        
                return bestValue, bestAction

        # Inicia a recursão na raiz da árvore: Pac-Man (agente 0), Profundidade Inicial (0) e Estado Atual
        _, action = minimax(0, 0, gameState)
        
        # Retorna apenas a ação calculada para o Pac-Man realizar no ambiente de jogo
        return action


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
        minFoodDistance = 0  # Se não houver mais comida, usamos 0 para não dar erro (o jogo provavelmente acabou)

    # 2. Avaliação de Fantasmas
    # Calcula a distância do fantasma que está mais perto do Pac-Man
    ghostDistances = [manhattanDistance(pos, ghost.getPosition()) for ghost in ghostStates]
    minGhostDistance = min(ghostDistances)

    # Verifica se os fantasmas estão assustados (quando o Pac-Man comeu uma pílula de poder / cápsula grande)
    scaredTimes = [ghostState.scaredTimer for ghostState in ghostStates]
    
    # Se algum fantasma está assustado (scaredTimer > 0), o Pac-Man não precisa fugir dele.
    if min(scaredTimes) > 0:
        minGhostDistance = 0  # Ignoramos a distância do fantasma para evitar penalizar o Pac-Man por se aproximar

    # 3. Fórmula da Pontuação Final
    # - currentGameState.getScore(): Nota base (pontuação intrínseca do próprio estado do jogo)
    # - (1.5 / (minFoodDistance + 1)): Bônus por se aproximar da comida. O "+1" evita divisão por zero.
    # - (2 / (minGhostDistance + 1)): Penalidade que cresce conforme o fantasma se aproxima.
    return currentGameState.getScore() - (1.5 / (minFoodDistance + 1)) + (2 / (minGhostDistance + 1))

# Abreviação da função de avaliação para facilitar seu uso como argumento nos testes
better = betterEvaluationFunction
