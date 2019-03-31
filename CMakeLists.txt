cmake_minimum_required(VERSION 3.13)
project(firefighterProblem)

set(CMAKE_CXX_STANDARD 17)

add_executable(firefighterProblem src/main.cpp src/instance.cpp src/instance.h src/graph.cpp src/graph.h)