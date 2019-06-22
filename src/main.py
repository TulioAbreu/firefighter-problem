from instance import Instance
from graph import Graph
from vertex import State, Vertex
import random
import copy
import time

def main():
    while True:
        instance = Instance()
        instance.readInstance('../instances/%s.txt' % str(2))

        start_time = time.time()
        survivedRounds = solve(instance)
        finish_time = time.time()
        print('Time = %s seconds' % str(finish_time-start_time))


def solve(instance:Instance):
    roundCount = 0
    print ('Grafo com %s vertices' % instance.getGraphVertexCount())
    while True:
        indexToBlock = 0
        if instance.getVertexCounterByState(State.UNTOUCHED) > 0:
            while True:
                indexToBlock = random.randint(0, instance.getGraphVertexCount() - 1)
                if instance.getVertex(indexToBlock).getState() == State.UNTOUCHED:
                    break
            instance.protectVertex(indexToBlock)
        if instance.nextRound() is not True:
            break
        roundCount += 1

    print ('Num. vertices queimados = %s' % instance.getVertexCounterByState(State.BURNT))
    if instance.getVertexCounterByState(State.BURNT) <= 97:
        input()
    for defVertex in instance.report:
        print("Vertex %s deffended in round %s" % (defVertex['index'], defVertex['round']))
    return roundCount


if __name__ == "__main__":
    main()