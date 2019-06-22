from graph import Graph
from vertex import Vertex, State

class Instance():
    def __init__(self):
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
        instFile = open(filepath, "r")
        self.numVertices = int(instFile.readline())
        self.startVertices(self.numVertices)

        self.numEdges = int(instFile.readline())
        self.numFire = int(instFile.readline())

        for _ in range(self.numFire):
            burntVertex = int(instFile.readline())
            self.fireList.append(burntVertex)
            self.graph.setVertexState(burntVertex, State.BURNT)
            # self.graph.getVertexByIndex(burntVertex).setState(State.BURNT)

        for _ in range(self.numEdges):
            source, target = [int(v) for v in instFile.readline().split(' ')]
            self.graph.vertices[source].addNeighbor(target)
            self.graph.vertices[target].addNeighbor(source)

    def startVertices(self, numVertices):
        for i in range(numVertices):
            self.graph.vertices.append(Vertex(i))

    def nextRound(self):
        """
            Calculate next round of vertices

            Returns
            ---
            bool : If something changed inside graph
        """
        initialList = self.fireList.copy()
        changed = False
        for fireIndex in initialList:
            changed = changed | self.propagateFire(fireIndex)
        self.roundNumber += 1
        return changed

    def propagateFire(self, fireIndex):
        """
            Propagate fire inside instance's graph.

            Returns
            ---
            bool : If something changed inside graph
        """
        changed = False
        burntVertex = self.graph.vertices[fireIndex]
        for neighbor in burntVertex.getNeighbors():
            neighborState = self.graph.getVertexByIndex(neighbor).getState()
            if neighborState == State.BURNT:
                pass
            elif neighborState == State.PROTECTED:
                pass
            elif neighborState == State.UNTOUCHED:
                self.graph.setVertexState(neighbor, State.BURNT)
                # self.graph.getVertexByIndex(neighbor).setState(State.BURNT)
                self.fireList.append(neighbor)
                self.burntVertices += 1
                changed = True
        # TODO: Remove this sort, TIME = $$
        self.fireList.sort()
        return changed

    def getVertexCounterByState(self, state):
        count = 0
        for vertex in self.graph.getVertices():
            if vertex.getState() == state:
                count += 1
        return count

    def protectVertex(self, index):
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

    def getGraphVertexCount(self):
        return self.graph.getVertexCount()