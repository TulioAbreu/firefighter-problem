#ifndef FIREFIGHTERPROBLEM_INSTANCE_H
#define FIREFIGHTERPROBLEM_INSTANCE_H

#include <vector>
#include <cstddef>
#include <string>

enum status {
    UNTOUCHED = 0,
    BURNT,
    DEFENDED
};

class Graph;

class Instance {
private:
    // Quantos vértices possui a instância
    size_t verticesCounter;

    // Quantas arestas possui a instância
    size_t edgesCounter;

    // Índice em que o fogo aparecerá
    size_t fireIndex;

    // Grafo de representação do problema
    Graph* graph;

    // Ordem de defesa dos vertices
    std::vector<size_t> defendedVertices;

    // Realiza a leitura do arquivo de instância
    void readInstaceFile(std::string filepath);

    // Leva o Grafo para o próximo estado do problema ao propagar o fogo
    void nextRound();

    // Defende o vértice ID
    bool defendVertex(size_t id);

    // Qt de vertices defendidos
    size_t getDefendedVerticesCounter() { return defendedVertices.size(); }

public:
    Instance();
    virtual ~Instance();

    // Faz a leitura do arquivo FILEPATH e inicializa os dados da instância
    void Start(std::string filepath);

    // Executa a solução do problema
    void Solve();

    // Imprime o relatorio
    void PrintResult();
};


#endif //FIREFIGHTERPROBLEM_INSTANCE_H
