#include <stdio.h>

// Use both absolute and relative include path
#include "seb/vehicle/apps/engine/Engine.h"
#include "../apps/engine/EngineBlock.h"
#include "../apps/engine/Piston.h"

int main()
{
    Piston piston(10, 15);
    EngineBlock engineBlock(8);
    Engine engine(&engineBlock, &piston);
    printf("I am a bus without engine power %d\n", engine.getPower());
}
