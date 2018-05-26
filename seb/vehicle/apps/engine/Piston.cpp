/*
 * Piston.cpp
 *
 *  Created on: Feb 23, 2018
 *      Author: thagen
 */

#include "Piston.h"

Piston::Piston(int width, int hight):
                m_width(width),
                m_hight(hight)
{
}

Piston::~Piston()
{
}

int Piston::getVolume()
{
    return m_width * m_hight;
}

