/*
 * Engine.cpp
 *
 *  Created on: Feb 23, 2018
 *      Author: thagen
 */

#include "Engine.h"

Engine::Engine(EngineBlock* engineBlock, Piston* piston):
               m_engineBlock(engineBlock),
               m_piston(piston)
{
}

Engine::~Engine()
{
}

int Engine::getPower()
{
    return m_engineBlock->getNumberOfPistons() * m_piston->getVolume();
}
