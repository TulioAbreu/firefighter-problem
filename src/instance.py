from graph import Graph
from vertex import Vertex, State

class Instance():
    def __init__(self):
        """
            Inicializa as variáveis de uma instância
        """
        self.graph = Graph()
        self.numVertices = 0
        self.numEdges = 0
        self.numFire = 0
        self.fireList = list()
        self.burntVertices = 0
        self.protectedVertices = list()
        self.roundNumber = 1
        self.report = []

    def readInstance(self, filepath:str):
        """
            Realiza a leitura de um arquivo de instância

            Parâmetros
            ---
            filepath: str - Caminho para o arquivo de instância
        """
        instFile = open(filepath, "r")
        self.numVertices = int(instFile.readline())
        self.startVertices(self.numVertices)

        self.numEdges = int(instFile.readline())
        self.numFire = int(instFile.readline())

        for _ in range(self.numFire):
            burntVertex = int(instFile.readline())
            self.fireList.append(burntVertex)
            self.graph.setVertexState(burntVertex, State.BURNT)

        for _ in range(self.numEdges):
            source, target = [int(v) for v in instFile.readline().split(' ')]
            self.graph.vertices[source].addNeighbor(target)
            self.graph.vertices[target].addNeighbor(source)

    def startVertices(self, numVertices: int):
        """
            Inicializa o grafo com N vertices vazios

            Parâmetros
            ---
            numVertices: int - Número de vértices a serem criados no grafo
        """
        for i in range(numVertices):
            self.graph.vertices.append(Vertex(i))

    def nextRound(self):
        """
            Leva a instância para o seu próximo round, propagando o fogo

            Retorna
            ---
            bool: O grafo foi modificado durante a expansão do fogo?
        """
        initialList = self.fireList.copy()
        changed = False
        for fireIndex in initialList:
            changed = changed | self.propagateFire(fireIndex)
        self.roundNumber += 1
        return changed

    def propagateFire(self, fireIndex):
        """
            Propaga o fogo dentro de um grafo

            Retorna
            ---
            bool: Retorna se o grafo foi modificado durante a expansão do fogo?
        """
        changed = False
        burntVertex = self.graph.getVertexByIndex(fireIndex)
        for neighbor in burntVertex.getNeighbors():
            neighborState = self.graph.getVertexByIndex(neighbor).getState()
            if neighborState == State.BURNT:
                pass
            elif neighborState == State.PROTECTED:
                pass
            elif neighborState == State.UNTOUCHED:
                self.graph.setVertexState(neighbor, State.BURNT)
                self.fireList.append(neighbor)
                self.burntVertices += 1
                changed = True
        return changed

    def getVertexCounterByState(self, state):
        count = 0
        for vertex in self.graph.getVertices():
            if vertex.getState() == state:
                count += 1
        return count

    def protectVertex(self, index):
        if self.graph.getVertexByIndex(index).getState() == State.UNTOUCHED:
            self.graph.setVertexState(index, State.PROTECTED)
            self.protectedVertices.append(index)
            self.report.append({
                'index': int(index),
                'round': int(self.roundNumber),
            })

    def getVertex(self, index):
        return self.graph.getVertexByIndex(index)

    def printReport(self):
        print ('Num. vertices queimados = %s' % self.getVertexCounterByState(State.BURNT))

        for defVertex in self.report:
            print("Vertex %s deffended in round %s" % (defVertex['index'], defVertex['round']))

    def getHeuristic(self):
        return self.getVertexCounterByState(State.BURNT)

    def getGraphVertexCount(self):
        return self.graph.getVertexCount()

    def filterUntouchedVertices(self) -> [int]:
        untouchedVertices = list()
        for i in range(self.graph.getVertexCount()):
            if self.graph.getVertexByIndex(i).getState() == State.UNTOUCHED:
                untouchedVertices.append(i)
        return untouchedVertices