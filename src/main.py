from instance import Instance
from vertex import State
from csvGenerator import CsvGenerator
from selector import BorderSelector, Selector
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
    instance.readInstance(filepath)

    start_time = time.time()
    result = solve(instance, start_time)
    finish_time = time.time()

    print('Numero de vertices queimados = %s/%s' %
        (instance.getVertexCounterByState(State.BURNT), 
         instance.getGraphVertexCount()))
    for roundReport in instance.report:
        print ('Vertice %s defendido no round %s' %
            (roundReport['index'], roundReport['round']))

    assert (finish_time-start_time) < 600.0  # Limite de 10 minutos
    print ('Time: %s' %  (finish_time-start_time))
    return instance


def solve(instance: Instance, startTime):
    """
        Soluciona uma dada instância

        Parâmetros
        ---
        Instance: instâcia a ser resolvida
    """
    FIREMEN_AMOUNT = 5

    while True:
        if instance.getVertexCounterByState(State.UNTOUCHED) > 0:
            selector = BorderSelector(instance, FIREMEN_AMOUNT)

            indexesToBlock = selector.selectDefenseVertex()
            assert len(indexesToBlock) <= FIREMEN_AMOUNT
            for i in indexesToBlock:
                instance.protectVertex(i)

        if instance.nextRound() is not True: # Se nao existe proximo round
            break


def saveCSV(instance: Instance, instNumber: int):
    """
        Realiza a preparação dos dados e os salva em um arquivo CSV

        Parâmetros
        ---
        instance: Instance - Instancia a ter seus resultados salvos
        instNumber: int - Numero da instancia a ser salva
    """
    headerElements = [
        'Round',
        'Vertice Defendido'
    ]

    dataMatrix = []
    for roundReport in instance.report:
        matrixLine = [
            roundReport['round'],
            roundReport['index']
        ]
        dataMatrix.append(matrixLine)

    saveFilepath = '../outputs/%s.csv' % instNumber
    CsvGenerator(saveFilepath, headerElements, dataMatrix).writeCSV()


if __name__ == "__main__":
    NUM_INSTANCES = 12

    for instanceNumber in range(1, NUM_INSTANCES+1):
        print ("Rodando instancia  %s/%s..." % (instanceNumber, NUM_INSTANCES))
        instFinalState = runInstance(instanceNumber)
        saveCSV(instFinalState, instanceNumber)
        print('---------------------------------------------------------------')

    print("Concluido!")
