#ifndef FIREFIGHTERPROBLEM_GRAPH_H
#define FIREFIGHTERPROBLEM_GRAPH_H

#include <vector>
#include <string>

class Vertex {
private:
    // ID do vértice
    size_t id;

    // Valor do vértice
    size_t value;

    // Lista de vizinhos do vértice
    std::vector<Vertex*> neighbors;

    // Modifica o ID do vértice para ID
    void setID(const size_t id) { this->id = id; }

public:
    Vertex(const size_t id, const size_t value);

    // Retorna o ID do vértice
    size_t getID() const { return this->id; }

    // Retorna o VALOR do vértice
    size_t getValue() const { return this->value; }

    // Modifica o VALOR do vértice para VALUE
    void setValue(const size_t value) { this->value = value; }

    // Adiciona um vizinho ao vértice
    void addNeighbor(Vertex* neighbor);

    // Retorna o início da lista de vizinhos
    std::vector<Vertex*>::iterator beginNeighbors();

    // Retorna o fim da lista de vizinhos
    std::vector<Vertex*>::iterator endNeighbors();

    // Retorna a string correspondente ao vértice
    std::string toString();
};

class Graph {
private:
    // Lista de vértices do Grafo
    std::vector<Vertex*> vertices;

public:
    Graph() {}
    ~Graph();

    // Adiciona uma aresta entre os vértices ID_V1 e ID_V2
    void addEdge(const size_t id_v1, const size_t id_v2);

    // Adiciona um vértice (ID, Value) no grafo
    void addVertex(const size_t id, const size_t value);

    // Retorna o início da lista de vértices do grafo
    std::vector<Vertex*>::iterator beginVertexNeighbors(size_t id);

    // Retorna o fim da lista de vértices do grafo
    std::vector<Vertex*>::iterator endVertexNeighbors(size_t id);

    // Modifica o valor do vértice ID para VALUE
    void setVertexValue(const size_t id, const size_t value);

    // Retorna o valor do vértice ID
    size_t getVertexValue(size_t id) const;

    // Retorna o numero de vertices no grafo
    size_t getVertexCounter() const { return this->vertices.size(); }

    // Retorna a string correspondente ao vértice
    std::string toString();
};


#endif //FIREFIGHTERPROBLEM_GRAPH_H
