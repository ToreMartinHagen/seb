/*
 * Wheel.cpp
 *
 *  Created on: Feb 23, 2018
 *      Author: thagen
 */

#include "Wheel.h"

Wheel::Wheel(int size): m_size(size)
{
}

Wheel::~Wheel()
{
}

int Wheel::getSize()
{
    return m_size;
}
