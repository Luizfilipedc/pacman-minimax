"""
Guia do Projeto: Implementação do Algoritmo Minimax para Pac-Man

Disciplina: Inteligência Artificial
Curso: Ciências da Computação
Professor: Nikson Bernardes Fernandes Ferreira

--------------------------------------------------
1. Introdução
--------------------------------------------------
Neste projeto, será implementado o algoritmo Minimax para controlar o agente Pac-Man
em um cenário dinâmico. O Pac-Man e os fantasmas são agentes que interagem no ambiente,
e o objetivo é fazer com que o Pac-Man tome decisões inteligentes.

--------------------------------------------------
2. Objetivo
--------------------------------------------------
Compreender profundamente o algoritmo Minimax, incluindo:
- Conceitos de maximização e minimização
- Aplicação prática em jogos de soma zero

--------------------------------------------------
3. O Algoritmo Minimax
--------------------------------------------------
Algoritmo recursivo usado em jogos de dois jogadores.

- Nó MAX (Pac-Man):
  Busca maximizar a pontuação.

- Nó MIN (Fantasmas):
  Busca minimizar a pontuação do Pac-Man.

--------------------------------------------------
4. Estrutura do Código
--------------------------------------------------
Arquivo principal: seuPacManAgents.py

Classe base:
class MinimaxAgent(MultiAgentSearchAgent):

Função principal:
def getAction(self, gameState):

Função auxiliar:
def minimax(agentIndex=0, depth=0, state=gameState):

--------------------------------------------------
5. Detalhes da Implementação
--------------------------------------------------

5.1 Parâmetros:
- agentIndex: indica o agente atual (0 = Pac-Man)
- depth: profundidade da árvore
- state: estado atual do jogo

5.2 Condição de parada:
- state.isWin() ou state.isLose()
- depth == self.depth

Retorno:
self.evaluationFunction(state)

5.3 Controle de agentes:
- Último fantasma → próximo agente = Pac-Man (0)
- Caso contrário → agentIndex + 1

Profundidade aumenta somente após todos os agentes jogarem.

--------------------------------------------------
5.4 Lógica de Maximização (Pac-Man)
--------------------------------------------------
- Inicializar valor máximo = -inf
- Para cada ação:
    - Gerar próximo estado
    - Chamar minimax recursivamente
    - Atualizar melhor valor e ação
- Retornar melhor ação (nível inicial) ou valor (recursão)

--------------------------------------------------
5.5 Lógica de Minimização (Fantasmas)
--------------------------------------------------
- Inicializar valor mínimo = +inf
- Para cada ação:
    - Gerar próximo estado
    - Chamar minimax recursivamente
    - Atualizar valor mínimo
- Retornar valor mínimo

--------------------------------------------------
6. Execução
--------------------------------------------------
Executar no terminal:

python3 pacman.py --pacman MinimaxAgent

Com profundidade:
python3 pacman.py --pacman MinimaxAgent --depth 2

--------------------------------------------------
7. Dicas
--------------------------------------------------
- Use self.evaluationFunction(state)
- self.index = 0 (Pac-Man)
- Teste com depth baixo (1 ou 2)
- Use print para debug
- Trate casos sem ações possíveis

--------------------------------------------------
8. Entrega
--------------------------------------------------
Arquivo:
seuPacManAgents.py com implementação completa

--------------------------------------------------
9. Critérios de Avaliação
--------------------------------------------------
- Correção do algoritmo
- Desempenho do Pac-Man
- Compreensão conceitual
- Qualidade do código

--------------------------------------------------
"""
