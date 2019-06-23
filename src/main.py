from instance import Instance
from vertex import State
import selector
import time


def runInstance(instanceNumber):
    instance = Instance()
    instance.readInstance('../instances/%s.txt' % str(instanceNumber))

    start_time = time.time()
    solve(instance)
    finish_time = time.time()
    instance.printReport()
    print('Time = %s seconds' % str(finish_time-start_time))
    assert (finish_time-start_time) < 600.0  # 10 min time limit


def selectDefenseVertex(instance:Instance) -> [int]:
    """
        This function defines how to select the vertex to defend on each round
    """
    return selector.MiniMaxSelector(instance, 3).selectDefenseVertex()
    # return [selector.RandomSelector(instance).selectDefenseVertex()]


def solve(instance:Instance):
    """
        This function is called to solve an instance
    """
    print ('Grafo com %s vertices' % instance.getGraphVertexCount())
    i = 0
    toBlock = []
    while True: # Finishes when there is no changes between two rounds
        if instance.getVertexCounterByState(State.UNTOUCHED) > 0:
            if len(toBlock) > 0:
                instance.protectVertex(toBlock.pop(0))
            else:
                indexesToBlock = selectDefenseVertex(instance)
                instance.protectVertex(indexesToBlock.pop(0))
                [toBlock.append(index) for index in indexesToBlock]
        if instance.nextRound() is not True:
            break
        i += 1


if __name__ == "__main__":
    for i in range(1, 12):
        print ('## Instance %s' % i)
        runInstance(9)
        print ('############################')
