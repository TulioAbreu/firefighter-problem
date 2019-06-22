from instance import Instance
from vertex import State
import selector
import time


def main():
    instance = Instance()
    instance.readInstance('../instances/%s.txt' % str(2))

    start_time = time.time()
    solve(instance)
    finish_time = time.time()
    instance.printReport()
    print('Time = %s seconds' % str(finish_time-start_time))


def selectDefenseVertex(instance:Instance):
    """
        This function defines how to select the vertex to defend on each round
    """
    return selector.MiniMaxSelector(instance).selectDefenseVertex()
    # return selector.RandomSelector(instance).selectDefenseVertex()

def solve(instance:Instance):
    """
        This function is called to solve an instance
    """
    print ('Grafo com %s vertices' % instance.getGraphVertexCount())
    while True: # Finishes when there is no changes between two rounds
        if instance.getVertexCounterByState(State.UNTOUCHED) > 0:
            indexToBlock = selectDefenseVertex(instance)
            instance.protectVertex(indexToBlock)
        if instance.nextRound() is not True:
            break


if __name__ == "__main__":
    main()
