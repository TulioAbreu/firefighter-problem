from abc import ABC, abstractmethod
from vertex import State
from instance import Instance

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


import copy
class MiniMaxSelector(Selector):
    def __init__(self, instance:Instance, maxDepth:int):
        super().__init__(instance)
        self.maxDepth = maxDepth
        self.maximizingPlayer = False
        self.alpha = float('-inf')
        self.beta = float('inf')

    def isTerminalNode(self):
        return self.instance.getVertexCounterByState(State.UNTOUCHED) == 0

    def getChildNodes(self, node:Instance):
        childNodes = list()
        untouchedVertices = node.filterUntouchedVertices() # Options to play
        minValue = float('inf')
        for untouchedVertex in untouchedVertices:
            nodeCopy = copy.deepcopy(node)
            nodeCopy.protectVertex(untouchedVertex)
            nodeCopy.nextRound()
            childNodes.append((nodeCopy, untouchedVertex))
            nodeValue = nodeCopy.getHeuristic()
            if nodeValue <= minValue:
                minValue = nodeValue
        return [node for node in childNodes if node[0].getHeuristic() <= minValue]

    def isGameOver(self, node:Instance):
        nodeCopy = copy.deepcopy(node)
        return nodeCopy.nextRound() is False

    def minimax(self, node:Instance, depth:int, path:[int], isMaximizingPlayer:bool):
        if depth == 0 or self.isGameOver(node):
            return node.getHeuristic(), path

        if isMaximizingPlayer:
            childNode = copy.deepcopy(node)
            childNode.nextRound()
            value, newPath = self.minimax(childNode, depth-1, path, False)
            self.alpha = max(self.alpha, value)
            return value, newPath
        else:
            bestValue = float('inf')
            pathToUse = []
            childNodePlays = node.filterUntouchedVertices()
            for childNodePlay in childNodePlays:
                childNode = copy.deepcopy(node)
                childNode.protectVertex(childNodePlay)
                value, usedPath = self.minimax(childNode, depth-1, path + [childNodePlay], True)
                if value <= bestValue:
                    bestValue = value
                    pathToUse = usedPath
                self.beta = min(self.beta, value)
                if self.beta < self.alpha:
                    print('Corte realizado')
                    break
            return bestValue, pathToUse

    def selectDefenseVertex(self):
        value, optimalPath = self.minimax(self.instance, self.maxDepth, [], False)
        print ('Optimal value =', value)
        print ('Optimal path =', optimalPath)
        print ('-------------------------------------------------')
        return optimalPath
