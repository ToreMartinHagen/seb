#include <stdio.h>

// Use both absolute and relative include path
#include <seb/vehicle/apps/wheel/Wheel.h>
#include <seb/vehicle/apps/engine/Engine.h>
#include "../apps/engine/EngineBlock.h"
#include "../apps/engine/Piston.h"

#include <seb/vehicle/apps/window/Front.gen.h>

int main()
{
    Wheel wheel(9);
    Piston piston(5, 4);
    EngineBlock engineBlock(8);
    Engine engine(&engineBlock, &piston);
    Front front;
    printf("I am a car with wheels size %d and engine power %d\n", wheel.getSize(), engine.getPower());
    printf("My front window is %s\n", front.getColor());
}
