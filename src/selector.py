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


class MiniMaxSelector(Selector):
    def __init__(self, instance, maxDepth):
        super().__init__(instance)
        self.maxDepth = maxDepth
        self.maximizingPlayer = False

    def isTerminalNode(self):
        raise NotImplementedError

    def getChildNodes(node:Instance):
        raise NotImplementedError

    # TODO: Get the chosen child node while getting minimax value!
    def minimax(node:Instance, depth, maximizingPlayer):
        if depth == 0 or isTerminalNode():
            return node.getHeuristic()
        if maximizingPlayer:
            value = int('inf')
            for childNode in getChildNodes(node):
                value = max(value, minimax(childNode, depth-1, False))
            return value
        else:
            value = -int('inf')
            for childNode in getChildNodes(node):
                value = min(value, minimax(childNode, depth-1, False))
            return value

    def selectDefenseVertex(self, instance:Instance):
        value, defendedVertices =  minimax(instance, self.maxDepth, False)
        return (value, defendedVertices)