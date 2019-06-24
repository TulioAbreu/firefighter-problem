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
