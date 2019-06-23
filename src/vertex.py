from enum import Enum
class State(Enum):
    UNTOUCHED = 0
    BURNT = 1
    PROTECTED = 2


class Vertex():
    def __init__(self, index):
        self.index = index
        self.state = State.UNTOUCHED
        self.neighbors = list()
    
    def getIndex(self) -> int:
        """
            Return vertex index from graph
        """
        return self.index
    
    def setState(self, state:State):
        """
            Set vertex State
        """
        self.state = state;
    
    def getState(self) -> State:
        """
            Get vertex State
        """
        return self.state

    def addNeighbor(self, index):
        """
            Add a neighbor (index) to vertex
        """
        self.neighbors.append(index)

    def getNeighbors(self) -> [int]:
        """
            Returns all vertex's neighbors (indexes)
        """
        return self.neighbors
    
    def __str__(self):
        stateStr = ""
        if self.state == State.UNTOUCHED:
            stateStr = "UNTOUCHED"
        elif self.state == State.BURNT:
            stateStr = "BURNT"
        elif self.state == State.PROTECTED:
            stateStr = "PROTECTED"
        return "Index=" + str(self.index) + "; State=" + stateStr + "; Neighbors=" + str(self.neighbors)
