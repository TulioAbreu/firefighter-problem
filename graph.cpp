#include "graph.h"

// 
// Implementação dos métodos da classe Vertex
// 

Vertex::Vertex(const size_t id, const size_t value)
{
    this->id = id;
    this->value = value;
}


void Vertex::addNeighbor(Vertex* neighbor)
{
    // Checa possível duplicata
    for (auto n : this->neighbors) {
        if (n->getID() == neighbor->getID()) {
            return;
        }
    }

    this->neighbors.push_back(neighbor);
}


std::vector<Vertex*>::iterator Vertex::beginNeighbors()
{
    return this->neighbors.begin();
}


std::vector<Vertex*>::iterator Vertex::endNeighbors()
{
    return this->neighbors.end();
}


// Retorna a string correspondente à lista de id dos vizinhos
static std::string getNeighborsStr(std::vector<Vertex*> neighbors) {
    std::string str = "";
    for (auto neighbor : neighbors) {
        str += std::to_string(neighbor->getID()) + ",";
    }
    if (str.length() > 2) {
        str = str.substr(0, str.length() - 1);
    }
    return str;
}


std::string Vertex::toString()
{
    std::string neighbors_str = getNeighborsStr(this->neighbors);
    return (
            "Vertex " + std::to_string(this->getID()) + " {" +\
        "Value=" + std::to_string(this->getValue()) +";" +\
        "Neighbors=[" + neighbors_str + "]}"
    );
}


std::vector<Vertex*>::iterator Graph::beginVertexNeighbors(size_t id)
{
    for (size_t i = 0; i < this->vertices.size(); ++i) {
        if (this->vertices[i]->getID() == id) {
            return this->vertices[i]->beginNeighbors();
        }
    }
    return this->vertices.at(0)->beginNeighbors();
}


std::vector<Vertex*>::iterator Graph::endVertexNeighbors(size_t id)
{
    for (auto vertex : this->vertices) {
        if (vertex->getID() == id) {
            return vertex->endNeighbors();
        }
    }
    return this->vertices.at(0)->endNeighbors();
}


void Graph::setVertexValue(const size_t id, const size_t value)
{
    for (size_t i = 0; i < this->vertices.size(); ++i) {
        if (vertices[i]->getID() == id) {
            vertices[i]->setValue(value);
        }
    }
}


size_t Graph::getVertexValue(size_t id) const
{
    for (size_t i = 0; i < this->vertices.size(); ++i) {
        if (vertices[i]->getID() == id) {
            return vertices[i]->getValue();
        }
    }
    return -1;
}


void Graph::addVertex(const size_t id, const size_t value)
{
    Vertex* vertex = new Vertex(id, value);
    this->vertices.push_back(vertex);
}


Graph::~Graph()
{
    for (std::vector<Vertex*>::iterator it = this->vertices.begin(); it != this->vertices.end(); ++it) {
        delete (*it);
    }
    this->vertices.clear();
}


void Graph::addEdge(const size_t id_v1, const size_t id_v2)
{
    Vertex* pV1 = nullptr;
    Vertex* pV2 = nullptr;
    for (auto vertex : this->vertices) {
        if (vertex->getID() == id_v1) {
            pV1 = vertex;
        }

        if (vertex->getID() == id_v2) {
            pV2 = vertex;
        }
    }

    if (pV1 == nullptr || pV2 == nullptr) {
        return;
    }

    pV1->addNeighbor(pV2);
    pV2->addNeighbor(pV1);
}

// Retorna a string correspondente ao conjunto de vertices
static std::string getVerticesStr(std::vector<Vertex*> vertices)
{
    std::string str = "";
    for (auto vertex : vertices) {
        str += vertex->toString() + ";\n\t";
    }
    if (str.length() > 2) {
        str = str.substr(0, str.length() - 1);
    }
    return str;
}


std::string Graph::toString()
{
    std::string str = getVerticesStr(this->vertices);
    return "Graph {\n\t" + str + "}";
}