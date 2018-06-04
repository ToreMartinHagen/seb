/*
 * EngineBlock.cpp
 *
 *  Created on: Feb 23, 2018
 *      Author: thagen
 */

#include "EngineBlock.h"

EngineBlock::EngineBlock(int numberOfPistons):
                        m_numberOfPistons(numberOfPistons)
{
}

EngineBlock::~EngineBlock()
{
}

int EngineBlock::getNumberOfPistons()
{
    return m_numberOfPistons;
}
