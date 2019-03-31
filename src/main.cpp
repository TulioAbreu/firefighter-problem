#include <iostream>
#include "instance.h"

int main() {
    Instance* instance = new Instance();
    instance->Start("../instances/1.txt");
    instance->Solve();
    instance->PrintResult();
    delete instance;
    return 0;
}