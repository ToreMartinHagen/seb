/*
 * Engine.h
 *
 *  Created on: Feb 23, 2018
 *      Author: thagen
 */

#ifndef SRC_SEB_VEHICLE_APPS_ENGINE_ENGINE_H_
#define SRC_SEB_VEHICLE_APPS_ENGINE_ENGINE_H_

#include "EngineBlock.h"
#include "Piston.h"


class Engine
{
public:
    Engine(EngineBlock* engineBlock, Piston* piston);
    virtual ~Engine();

    int getPower();

private:
    EngineBlock* m_engineBlock;
    Piston* m_piston;
};

#endif /* SRC_SEB_VEHICLE_APPS_ENGINE_ENGINE_H_ */
