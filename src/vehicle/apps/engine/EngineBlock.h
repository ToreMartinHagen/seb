/*
 * EngineBlock.h
 *
 *  Created on: Feb 23, 2018
 *      Author: thagen
 */

#ifndef SRC_SEB_VEHICLE_APPS_ENGINE_ENGINEBLOCK_H_
#define SRC_SEB_VEHICLE_APPS_ENGINE_ENGINEBLOCK_H_

class EngineBlock
{
public:
    EngineBlock(int numberOfPistons);
    virtual ~EngineBlock();

    int getNumberOfPistons();
private:
    int m_numberOfPistons;
};

#endif /* SRC_SEB_VEHICLE_APPS_ENGINE_ENGINEBLOCK_H_ */
