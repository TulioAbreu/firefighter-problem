from instance import Instance
from vertex import State
from csvGenerator import CsvGenerator
import selector
import time


def runInstance(instanceNumber: int) -> (Instance, float):
    """
        Realiza a leitura e a execução de uma instância
        Parâmetros
        ---
        int: número da instância a ser executada

        Retorna
        ---
        Instance: instância em seu estado final
        float: tempo de execução
    """
    instance = Instance()
    filepath = '../instances/%s.txt' % instanceNumber
    print('Lendo o arquivo de instancia... (%s)' % filepath)
    instance.readInstance(filepath)
    print ('Graph with %s vertices' % instance.getGraphVertexCount())
    start_time = time.time()
    result = solve(instance, start_time)
    finish_time = time.time()

    instance.printReport()
    print('Time = %s seconds' % str(finish_time-start_time))
    assert (finish_time-start_time) < 600.0  # 10 min time limit

    if result is not None:
        return (result, finish_time-start_time)
    else:
        return (instance, finish_time-start_time)


def solve(instance: Instance, startTime):
    """
        Soluciona uma dada instância

        Parâmetros
        ---
        Instance: instâcia a ser resolvida
    """
    FIREMEN_AMOUNT = 5
    MINIMAX_MAX_DEPTH = 4
    toBlock = []
    return selector.BranchAndBoundSelector(instance, startTime).selectDefenseVertex()

    # while True:
    #     if instance.getVertexCounterByState(State.UNTOUCHED) > 0:
    #         for i in range(FIREMEN_AMOUNT):
    #             if len(toBlock) > 0:
    #                 instance.protectVertex(toBlock.pop(0))
    #             else:
    #                 indexesToBlock = selector.MiniMaxSelector(instance, MINIMAX_MAX_DEPTH).selectDefenseVertex()
    #                 if indexesToBlock != []:
    #                     instance.protectVertex(indexesToBlock.pop(0))
    #                     [toBlock.append(index) for index in indexesToBlock]
    #     # Propaga o fogo e retorna se existe um proximo round
    #     if instance.nextRound() is not True:
    #         # Se nao existe um proximo round o loop é finalizado
    #         break


def saveCSV(results: [(Instance, float)]):
    """
        Realiza a preparação dos dados e os salva em um arquivo CSV

        Parâmetros
        ---
        [Instancia, float]: Lista contendo instâncias em seus estados finais e
                            seus respectivos tempos de execução
    """
    headerElements = [
        'Instância',
        'Vértices Queimados',
        'Total de Vértices',
        'Defesas por Round',
        'Tempo de Execução'
    ]
    dataMatrix = []
    for i, (instance, execTime) in enumerate(results):
        matrixLine = [
            i+1,                                            # Instância
            instance.getVertexCounterByState(State.BURNT),  # Vertices Queimados
            instance.getGraphVertexCount(),                 # Total de Vertices
            defPerRoundScript(instance),                    # Defesas por Round
            str(round(execTime, 4)).replace('.', ',')       # Tempo de execução
        ]
        dataMatrix.append(matrixLine)

    CsvGenerator('../output.csv', headerElements, dataMatrix).writeCSV()


def defPerRoundScript(instance: Instance) -> str:
    """
        Formata uma string contendo os vértices defendidos a cada round
        
        Parâmetros
        ---
        Instance: instância em seu estado final

        Retorna
        ---
        str: string contendo vértices defendidos a cada round
    """
    numRounds = max(instance.report, key=lambda x:x['round'])['round']
    finalStr = ""
    for i in range(numRounds):
        roundNum = i+1
        protected = [str(e['index']) for e in instance.report 
                                        if e['round'] == roundNum]
        finalStr += 'Round %s (%s)  ' % (roundNum, ", ".join(protected))
    return finalStr


if __name__ == "__main__":
    results = list()
    for i in range(1, 12):
        print ('## Instance %s' % i)
        results.append(runInstance(i))
        print ('###################################################################################################')
    saveCSV(results)
