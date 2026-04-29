# keyboardAgents.py
# -----------------
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
from game import Directions
import random


class KeyboardAgent(Agent):
    """
    Um agente controlado pelo teclado do usuário.
    """
    # NOTA: As teclas de setas também funcionam.
    WEST_KEY = 'a'
    EAST_KEY = 'd'
    NORTH_KEY = 'w'
    SOUTH_KEY = 's'
    STOP_KEY = 'q'

    def __init__(self, index=0):
        self.lastMove = Directions.STOP
        self.index = index
        self.keys = []

    def getAction(self, state):
        from graphicsUtils import keys_waiting
        from graphicsUtils import keys_pressed
        
        # Pega as teclas que foram pressionadas pelo jogador
        keys = keys_waiting() + keys_pressed()
        if keys != []:
            self.keys = keys

        legal = state.getLegalActions(self.index)
        move = self.getMove(legal)

        # Se nenhuma direção foi definida, tenta manter o último movimento
        if move == Directions.STOP:
            # Tenta se mover na mesma direção de antes
            if self.lastMove in legal:
                move = self.lastMove

        # Força o 'Stop' (parada) se a tecla de parada for pressionada e for uma ação legal
        if (self.STOP_KEY in self.keys) and Directions.STOP in legal:
            move = Directions.STOP

        # Se o movimento não for permitido pelas paredes, escolhe uma ação aleatória
        if move not in legal:
            move = random.choice(legal)

        self.lastMove = move
        return move

    def getMove(self, legal):
        """
        Retorna a direção baseada nas teclas pressionadas que também seja legal.
        """
        move = Directions.STOP
        if (self.WEST_KEY in self.keys or 'Left' in self.keys) and Directions.WEST in legal:
            move = Directions.WEST
        if (self.EAST_KEY in self.keys or 'Right' in self.keys) and Directions.EAST in legal:
            move = Directions.EAST
        if (self.NORTH_KEY in self.keys or 'Up' in self.keys) and Directions.NORTH in legal:
            move = Directions.NORTH
        if (self.SOUTH_KEY in self.keys or 'Down' in self.keys) and Directions.SOUTH in legal:
            move = Directions.SOUTH
        return move


class KeyboardAgent2(KeyboardAgent):
    """
    Um segundo agente controlado pelo teclado, feito para permitir
    multiplayer no mesmo computador.
    """
    # NOTA: Usar teclas diferentes (I, J, K, L) para o Jogador 2
    WEST_KEY = 'j'
    EAST_KEY = "l"
    NORTH_KEY = 'i'
    SOUTH_KEY = 'k'
    STOP_KEY = 'u'

    def getMove(self, legal):
        """
        Igual ao do primeiro jogador, mas sem aceitar as setas do teclado (que ficam pro Jogador 1).
        """
        move = Directions.STOP
        if (self.WEST_KEY in self.keys) and Directions.WEST in legal:
            move = Directions.WEST
        if (self.EAST_KEY in self.keys) and Directions.EAST in legal:
            move = Directions.EAST
        if (self.NORTH_KEY in self.keys) and Directions.NORTH in legal:
            move = Directions.NORTH
        if (self.SOUTH_KEY in self.keys) and Directions.SOUTH in legal:
            move = Directions.SOUTH
        return move
