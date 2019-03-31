#include "instance.h"
#include "graph.h"
#include <dirent.h>
#include <cassert>
#include <iostream>
#include <fstream>

Instance::Instance()
{
    this->graph = nullptr;
    this->edgesCounter = 0;
    this->fireIndex = 0;
    this->verticesCounter = 0;
    this->instanceFilepath = "";
}

Instance::~Instance()
{
    delete this->graph;
}


void Instance::Start(std::string filepath)
{
    this->graph = new Graph();
    if (this->instanceFilepath == "") {
        this->readInstaceFile(filepath);
    }
    else {
        this->readInstaceFile(this->instanceFilepath);
    }
    this->graph->setVertexValue(this->fireIndex, BURNT); // Queima o primeiro vértice
}


void Instance::readInstaceFile(std::string filepath)
{
    std::cout << "Reading instance file (" << filepath << ")" << std::endl;
    assert (filepath.size() > 0); // Confirma que foi passado um caminho para o arquivo

    std::ifstream instanceFile(filepath);
    assert(instanceFile.is_open()); // Confirma se o arquivo está aberto

    instanceFile >> this->verticesCounter;
    // Cria VERTICESCOUNTER vértices no Grafo em seu estado inicial
    for (size_t i = 0; i < this->verticesCounter; ++i) {
        this->graph->addVertex(i, UNTOUCHED);
    }

    instanceFile >> this->edgesCounter;
    instanceFile >> this->fireIndex; // Pula uma palavra
    instanceFile >> this->fireIndex;
    // Leitura e criação das arestas do arquivo de instância
    for (size_t i = 0; i < this->edgesCounter; ++i) {
        int vertex1, vertex2;
        instanceFile >> vertex1 >> vertex2;
        this->graph->addEdge(vertex1, vertex2);
    }
}


void Instance::Solve()
{
    assert (this->graph);
    assert (this->fireIndex >= 0);
    nextRound();
//    std::cout << this->graph->toString() << std::endl;
}


// Verifica se VALUE está presente em ARR
static bool isInArray(std::vector<size_t> arr, size_t value) {
    for (auto element : arr) {
        if (element == value) {
            return true;
        }
    }
    return false;
}


void Instance::nextRound()
{
    std::vector<size_t> neighbors2burn;
    // Cria a lista de vizinhos que serão queimados
    for (size_t i = 0; i < this->verticesCounter; ++i) {
        if (this->graph->getVertexValue(i) == BURNT) {
            for (
                    auto it = this->graph->beginVertexNeighbors(i);
                    it != this->graph->endVertexNeighbors(i);
                    ++it
                    ) {
                const int neighborID = (*it)->getID();
                if (! isInArray(neighbors2burn, neighborID)) {
                    neighbors2burn.push_back(neighborID);
                }
            }
        }
    }

    // Queima os vizinhos que não foram defendidos
    for (size_t i = 0; i < neighbors2burn.size(); ++i) {
        if (this->graph->getVertexValue(neighbors2burn[i]) != DEFENDED) {
            this->graph->setVertexValue(neighbors2burn[i], BURNT);
        }
    }
}

bool Instance::defendVertex(size_t id)
{
    switch(this->graph->getVertexValue(id)) {
        case UNTOUCHED: {
            this->graph->setVertexValue(id, DEFENDED);
            this->defendedVertices.push_back(id);
            return true;
        } break;
        case BURNT: {
            std::cout << "[Erro] Este vertice ja foi queimado." << std::endl;
        } break;
        case DEFENDED: {
            std::cout << "[Erro] Este vertice ja foi defendido" << std::endl;
        } break;
    }
    return false;
}


static size_t getBurntVertices(Graph* graph) {
    size_t counter = 0;
    for (size_t i = 0; i < graph->getVertexCounter(); ++i) {
        if (graph->getVertexValue(graph->getVertexValue(i)) == BURNT) {
            counter ++;
        }
    }
    return counter;
}

void Instance::PrintResult()
{
    if (this->defendedVertices.size() == 0) {
        std::cout << "[DEBUG] Nenhum vertice foi queimado." << std::endl;
        return;
    }
    std::cout << "Nro de vertices queimados = " << getBurntVertices(this->graph) << std::endl;

    std::cout << "Round - Vertice defendido" << std::endl;
    for (size_t i = 0; i < this->defendedVertices.size(); ++i) {
        std::cout << (i + 1) << " - " << this->defendedVertices[i] << std::endl;
    }

}

static std::vector<std::string> getInstanceFiles(std::string folderPath)
{
    std::vector<std::string> instance_files;
    DIR* dir;
    struct dirent* ent;
    if ((dir = opendir(folderPath.c_str())) != nullptr) {
        while ((ent = readdir(dir)) != nullptr) {
            instance_files.emplace_back(ent->d_name);
        }
        closedir(dir);
    } else {
        std::cout << "[error] Nao foi possivel abrir a pasta indicada." << std::endl;
    }

    return instance_files;
}


void Instance::Selector()
{
    std::string folderPath = "../instances/";
    std::vector<std::string> instanceFiles(getInstanceFiles(folderPath));
    instanceFiles.erase(instanceFiles.begin(), instanceFiles.begin() + 2); // Remove "." and ".."
    std::cout << "Selecione o arquivo de instancia: " << std::endl;
    int count = 0;
    for (size_t i = 0; i < instanceFiles.size(); ++i) {
        std::cout << i << ". " << instanceFiles.at(i) << "\t";
        count ++;
        if (count % 3 == 0 && i > 1) {
            std::cout << std::endl;
            count = 0;
        }
    }
    
    int index;
    std::cin >> index;
    
    if (index < 0 || index >= instanceFiles.size()) {
        std::cout << "[error] Indice de arquivo invalido." << std::endl;
    }
    else {
        this->instanceFilepath = folderPath + instanceFiles.at(index);
    }
}