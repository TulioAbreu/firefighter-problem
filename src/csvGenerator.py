class CsvGenerator():
    def __init__(self, savePath:str, headerElements:[str], dataMatrix):
        """
            Parâmetros
            ---
            savePath: str - Caminho e nome do arquivo CSV a ser salvo
            headerElements: [str] - Nome de cada coluna do arquivo CSV
            dataMatrix - Matriz contendo os dados a serem salvos
        """
        self.savePath = savePath
        self.headerElements = headerElements
        self.dataMatrix = dataMatrix

    def writeCSV(self):
        """
            Escreve um arquivo CSV a partir do caminho, dos elementos de header
            e da matriz de dados fornecidos no construtor
        """
        file = open(self.savePath, 'w')
        file.write("; ".join(self.headerElements) + '\n')
        for lineData in self.dataMatrix:
            lineDataStr = [str(data) for data in lineData]
            lineStr = "; ".join(lineDataStr) + '\n'
            file.write(lineStr)
        file.close()
