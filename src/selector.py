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
        self.play = None

    def isTerminalNode(self):
        return self.instance.getVertexCounterByState(State.UNTOUCHED) == 0

    def getChildNodes(self, node:Instance):
        childNodes = list()
        untouchedVertices = node.filterUntouchedVertices() # Options to play
        # Advance a state on simulation for each option
        for untouchedVertex in untouchedVertices:
            nodeCopy = copy.deepcopy(node)
            nodeCopy.protectVertex(untouchedVertex)
            nodeCopy.nextRound()
            childNodes.append((nodeCopy, untouchedVertex))
        return childNodes

    def isLeafNode(self, childNodes, depth):
        return depth == 0 or childNodes == []

    def minimax(self, node:Instance, depth:int, path:[int]):
        childNodes = self.getChildNodes(node)

        if self.isLeafNode(childNodes, depth):
            return node.getHeuristic(), path

        else:
            bestValue = float('inf')
            pathToUse = []
            for childNode, chosenVertex in childNodes:
                minmaxValue, usedPath = self.minimax(childNode, depth-1, path + [chosenVertex])

                if bestValue >= minmaxValue:
                    bestValue = minmaxValue
                    pathToUse = usedPath

            return bestValue, pathToUse

    def selectDefenseVertex(self):
        _, optimalPath = self.minimax(self.instance, self.maxDepth, [])
        return optimalPath[0]
