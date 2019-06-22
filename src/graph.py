from vertex import (
    State,
    Vertex
)

class Graph():
    def __init__(self):
        self.vertices = list()

    def getVertexByIndex(self, index:int):
        """
            Returns a graph's vertex by index
        """
        return self.vertices[index]

    def getVertexCount(self) -> int:
        """
            Returns graph's vertices counter
        """
        return len(self.vertices)

    def getVertices(self) -> [Vertex]:
        """
            Return graph's vertices
        """
        return self.vertices

    def setVertexState(self, index, state):
        """
            Set a vertex state
        """
        assert index >= 0 & index < len(self.vertices)
        self.vertices[index].setState(state)

    def __str__(self):
        finalStr = "Graph {\n"
        for vertex in self.vertices:
            finalStr += '    ' + str(vertex) + '\n'
        finalStr = finalStr + '}'
        return finalStr
