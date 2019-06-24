from vertex import (
    State,
    Vertex
)

class Graph():
    def __init__(self):
        """
            Inicializa um grafo
        """
        self.vertices = list()

    def getVertexByIndex(self, index:int) -> Vertex:
        """
            Retorna um vértice do grafo pelo seu índice

            Parâmetros
            ---
            index:int - Índice do vértice a ser retornado

            Retorna
            ---
            Vertex: Vértice do de índice *index*
        """
        return self.vertices[index]

    def getVertexCount(self) -> int:
        """
            Retorna a quantidade de vértices do grafo

            Retorna
            ---
            int: Quantidade de vértices presentes no grafo
        """
        return len(self.vertices)

    def getVertices(self) -> [Vertex]:
        """
            Retorna todos os vértices do grafo

            Retorna
            ---
            [Vertex]: Vértices presentes no grafo
        """
        return self.vertices

    def setVertexState(self, index: int, state: State):
        """
            Modifica o estado de um vértice do grafo

            Parâmetros
            ---
            index:int - Índice do vértice a ser modificado
            state:State - Novo estado do vértice
        """
        assert index >= 0 & index < len(self.vertices)
        self.vertices[index].setState(state)

    def __str__(self):
        finalStr = "Graph {\n"
        for vertex in self.vertices:
            finalStr += '    %s\n' % str(vertex)
        finalStr = finalStr + '}'
        return finalStr
