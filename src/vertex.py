from enum import Enum
class State(Enum):
    UNTOUCHED = 0
    BURNT = 1
    PROTECTED = 2


class Vertex():
    def __init__(self, index):
        """
            Inicializa um vértice com um índicee um estado intocado
        """
        self.index = index
        self.state = State.UNTOUCHED
        self.neighbors = list()
    
    def getIndex(self) -> int:
        """
            Retorna
            ---
            int: Retorna o índice do vértice
        """
        return self.index
    
    def setState(self, state:State):
        """
            Modifica o estado atual do vértice

            Parâmetros
            ---
            state:State - Novo estado do vértice
        """
        assert self.state == State.UNTOUCHED
        self.state = state;
    
    def getState(self) -> State:
        """
            Retorna
            ---
            State: Estado atual do vértice
        """
        return self.state

    def addNeighbor(self, index: int):
        """
            Adiciona um vizinho ao vértice
            
            Parâmetros
            ---
            index: int - Indice do novo vizinho do vertice
        """
        self.neighbors.append(index)

    def getNeighbors(self) -> [int]:
        """
            Retorna
            ---
            int: Indice de todos os vizinhos do vértice
        """
        return self.neighbors
    
    def __str__(self):
        stateStr = ""
        if self.state == State.UNTOUCHED:
            stateStr = "UNTOUCHED"
        elif self.state == State.BURNT:
            stateStr = "BURNT"
        elif self.state == State.PROTECTED:
            stateStr = "PROTECTED"
        return 'Index=%s; State=%s; Neighbors=%s' % (
            self.index,
            stateStr,
            self.neighbors
        )
