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

    def isTerminalNode(self):
        return self.instance.getVertexCounterByState(State.UNTOUCHED) == 0

    def getChildNodes(self, node:Instance):
        childNodes = list()
        untouchedVertices = node.filterUntouchedVertices()
        for untouchedVertex in untouchedVertices:
            nodeCopy = copy.deepcopy(node)
            nodeCopy.graph.setVertexState(untouchedVertex, State.PROTECTED)
            nodeCopy.nextRound()
            childNodes.append(nodeCopy)
        return childNodes

    # TODO: Get the chosen child node while getting minimax value!
    def minimax(self, node:Instance, depth, maximizingPlayer):
        if depth == 0 or self.isTerminalNode():
            return node.getHeuristic()

        if maximizingPlayer:
            value = float('-inf')
            for childNode in getChildNodes(node):
                value = max(value, minimax(childNode, depth-1, False))
            return value
        else:
            value = float('inf')
            for childNode in self.getChildNodes(node):
                value = min(value, self.minimax(childNode, depth-1, False))
            return value

    def selectDefenseVertex(self):
        print(self.minimax(self.instance, self.maxDepth, False))
        return (value, defendedVertices)