from abc import ABC, abstractmethod
from vertex import State, Vertex
from instance import Instance
from utils import Stack

class Selector(ABC):
    def __init__(self, instance):
        self.instance = instance
    
    @abstractmethod
    def selectDefenseVertex(self):
        pass


import random
class RandomSelector(Selector):
    def __init__(self, instance):
        super().__init__(instance)

    def selectDefenseVertex(self):
        indexToBlock = 0
        while True:
            indexToBlock = random.randint(0, self.instance.getGraphVertexCount() - 1)
            if self.instance.getVertex(indexToBlock).getState() == State.UNTOUCHED:
                break
        return indexToBlock


import time
class BranchAndBoundSelector(Selector):
    def __init__(self, instance: Instance, startTime):
        super().__init__(instance)
        self.startTime = startTime

    def selectDefenseVertex(self):
        result = self.branchAndBound(self.instance)
        print(result.printReport())
        return result

    def heuristicSolution(self):
        return self.instance.getGraphVertexCount()

    def objectiveFunction(self, instance: Instance):
        return instance.getVertexCounterByState(State.BURNT)

    def generateChildNodes(self, node: Instance, depth: int):
        if depth % 5 == 0 and depth != 0:
            childNode = copy.deepcopy(node)
            childNode.nextRound()
            return [childNode]
        else:
            untouchedVertices = [vertex.getIndex() for vertex in node.graph.vertices if vertex.getState() == State.UNTOUCHED]
            childNodes = list()
            for untouchedVertex in untouchedVertices:
                childNode = copy.deepcopy(node)
                childNode.protectVertex(untouchedVertex)
                childNodes.append(childNode)
            return childNodes

    def representsCandidate(self, node:Instance):
        nodeCopy = copy.deepcopy(node)
        return nodeCopy.nextRound() is False

    def lowerBoundFunction(self, node: Instance):
        return node.getVertexCounterByState(State.UNTOUCHED)*0.90 + node.getVertexCounterByState(State.BURNT)

    def branchAndBound(self, node):
        problemUpperBound = self.heuristicSolution()
        # print('Initial upper bound = %s' % problemUpperBound)
        currentOptimum = copy.deepcopy(node)
        candidateQueue = Stack()
        candidateQueue.add((node, 0))
        while True and time.time()-self.startTime<60:
            assert not candidateQueue.empty()
            currNode, depth = candidateQueue.remove()
            if self.representsCandidate(currNode):
                if self.objectiveFunction(currNode) < problemUpperBound:
                    currentOptimum = copy.deepcopy(currNode)
                    problemUpperBound = self.objectiveFunction(currentOptimum)
                    # print('Current optimum updated: %s' % currentOptimum.getHeuristic())
                    # print(problemUpperBound)
            else:
                for childBranch in self.generateChildNodes(currNode, depth):
                    if self.lowerBoundFunction(childBranch) < problemUpperBound:
                        candidateQueue.add((childBranch, depth+1))

            if candidateQueue.empty():
                break

        return currentOptimum


import copy
from math import inf
class MiniMaxSelector(Selector):
    def __init__(self, instance:Instance, maxDepth:int):
        super().__init__(instance)
        self.maxDepth = maxDepth
        self.maximizingPlayer = False
        self.counter = 5
        self.alpha = -inf
        self.beta = inf

    def isGameOver(self, node:Instance):
        nodeCopy = copy.deepcopy(node)
        return nodeCopy.nextRound() is False

    def minimax(self, node:Instance, depth:int, path:[int], isMaximizingPlayer:bool):
    # def minimax(self, node:Instance, depth:int, path:[int], isMaximizingPlayer:bool, alpha, beta):
        if depth == 0 or self.isGameOver(node):
            return node.getHeuristic(), path

        if isMaximizingPlayer:
            childNode = copy.deepcopy(node)
            childNode.nextRound()
            self.counter = 5
            # value, newPath = self.minimax(childNode, depth-1, path, False, alpha, beta)
            value, newPath = self.minimax(childNode, depth-1, path, False)
            # alpha = max(alpha, value)
            self.alpha = max(self.alpha, value)
            return value, newPath
        else:
            bestValue = float('inf')
            pathToUse = []
            childNodePlays = node.filterUntouchedVertices()

            for childNodePlay in childNodePlays:
                childNode = copy.deepcopy(node)
                childNode.protectVertex(childNodePlay)
                if self.counter <= 0:
                    # value, usedPath = self.minimax(childNode, depth-1, path + [childNodePlay], True, alpha, beta)
                    value, usedPath = self.minimax(childNode, depth-1, path + [childNodePlay], True)
                else:
                    self.counter -= 1
                    # value, usedPath = self.minimax(childNode, depth, path + [childNodePlay], False, alpha, beta)
                    value, usedPath = self.minimax(childNode, depth, path + [childNodePlay], False)
                if value < bestValue:
                    bestValue = value
                    pathToUse = usedPath
                # beta = min(beta, value)
                # if alpha >= beta:
                self.beta = min(self.beta, value)
                if self.alpha >= self.beta:
                    break
            return bestValue, pathToUse

    def selectDefenseVertex(self):
        # value, optimalPath = self.minimax(self.instance, self.maxDepth, [], False, float('-inf'), float('inf'))
        value, optimalPath = self.minimax(self.instance, self.maxDepth, [], False)
        # print ('Optimal value =', value)
        # print ('Optimal path =', optimalPath)
        # print ('-------------------------------------------------')
        return optimalPath


class BorderSelector(Selector):
    def __init__(self, instance: Instance, FIREMEN_AMOUNT: int):
        """
            Parametros
            ---
            instance: Instance - Instancia a ser processada
            FIREMEN_AMOUNT: int - Numero de bombeiros
        """
        super().__init__(instance)
        self.FIREMEN_AMOUNT = FIREMEN_AMOUNT

    def selectDefenseVertex(self):
        """
            Retorna
            ---
            [int] - Retorna uma lista de tamanho FIREMEN_AMOUNT que corresponde
                    aos vertices a serem defendidos em um dado round
        """
        borderVertices = list()
        graphVertices = self.instance.graph.getVertices()
        burntVertices = [v for v in graphVertices
                           if v.getState() == State.BURNT]

        # Recebe todos os vizinhos INTOCADOS dos vertices pegando fogo
        for burntVertex in burntVertices:
            neighbors = burntVertex.getNeighbors()
            [borderVertices.append(n) for n in neighbors]
        borderVertices = list(set(borderVertices))
        borderVertices = [v for v in borderVertices
                            if graphVertices[v].getState() == State.UNTOUCHED]

        numNeighbors = [self.getNumNeighbors(b) for b in borderVertices]

        threatenedVertices = list(zip(borderVertices, numNeighbors))
        threatenedVertices.sort(key=lambda x:x[1], reverse=True)

        return [v[0] for v in threatenedVertices[:self.FIREMEN_AMOUNT]]


    def getNumNeighbors(self, vertexIndex: int):
        """
            Parametros
            ---
            vertexIndex:int - Indice de um vertice

            Retorna
            ---
            int - Grau do vertice passado por parametro
                  (DESCONSIDERA VIZINHOS BURNT OU PROTECTED)
        """
        neighborsCounter = 0

        vertex = self.instance.getVertex(vertexIndex)
        for neighbor in vertex.getNeighbors():
            if self.instance.getVertex(neighbor).getState() == State.UNTOUCHED:
                neighborsCounter += 1

        return neighborsCounter
