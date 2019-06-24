from instance import Instance
from vertex import State
import selector
import time


def runInstance(instanceNumber):
    instance = Instance()
    print('Reading file ../instances/%s.txt' % str(instanceNumber))
    instance.readInstance('../instances/%s.txt' % str(instanceNumber))

    start_time = time.time()
    solve(instance)
    finish_time = time.time()
    instance.printReport()
    print('Time = %s seconds' % str(finish_time-start_time))
    assert (finish_time-start_time) < 600.0  # 10 min time limit
    return (instance, finish_time-start_time)


def selectDefenseVertex(instance:Instance) -> [int]:
    """
        This function defines how to select the vertex to defend on each round
    """
    # return [int(input("Digite um numero para defesa: "))]
    return selector.MiniMaxSelector(instance, 3).selectDefenseVertex()
    # return [selector.RandomSelector(instance).selectDefenseVertex()]


def solve(instance:Instance):
    """
        This function is called to solve an instance
    """
    print ('Graph has %s vertices' % instance.getGraphVertexCount())

    i = 0
    toBlock = []
    while True: # Finishes when there is no changes between two rounds
        if instance.getVertexCounterByState(State.UNTOUCHED) > 0:
            for i in range(5):
                if len(toBlock) > 0:
                    instance.protectVertex(toBlock.pop(0))
                else:
                    indexesToBlock = selectDefenseVertex(instance)
                    if indexesToBlock != []:
                        instance.protectVertex(indexesToBlock.pop(0))
                        # instance.protectVertex(indexesToBlock.pop(0))
                        [toBlock.append(index) for index in indexesToBlock]
        if instance.nextRound() is not True:
            break
        i += 1


def saveCSV(results):
    file = open("../output.csv", "w")
    file.write('Instância; Vertices Queimados; Total de Vertices; Defendidos por Round; Tempo\n')
    for i, (instance, time) in enumerate(results):
        line = '%s; %s; %s; %s; %s\n' % (
            str(i+1),
            instance.getVertexCounterByState(State.BURNT),
            instance.getGraphVertexCount(),
            defPerRoundScript(instance),
            str(time)
        )
        file.write(line)
    file.close()


def defPerRoundScript(instance:Instance):
    numRounds = max(instance.report, key=lambda x:x['round'])['round']
    finalStr = ""
    for i in range(numRounds):
        roundNum = i+1
        protected = [str(e['index']) for e in instance.report if e['round'] == roundNum]
        finalStr += ('Round %s (' % str(roundNum)) + ", ".join(protected) + ')  '
    return finalStr
    # print("Vertex %s deffended in round %s" % (defVertex['index'], defVertex['round']))


if __name__ == "__main__":
    results = list()
    for i in range(1, 12):
        print ('## Instance %s' % i)
        results.append(runInstance(i))
        print ('###################################################################################################')
    saveCSV(results)
