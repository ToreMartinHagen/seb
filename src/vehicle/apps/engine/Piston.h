/*
 * Piston.h
 *
 *  Created on: Feb 23, 2018
 *      Author: thagen
 */

#ifndef SRC_SEB_VEHICLE_APPS_ENGINE_PISTON_H_
#define SRC_SEB_VEHICLE_APPS_ENGINE_PISTON_H_

class Piston
{
public:
    Piston(int width, int hight);
    virtual ~Piston();

    int getVolume();

private:
    int m_width;
    int m_hight;
};

#endif /* SRC_SEB_VEHICLE_APPS_ENGINE_PISTON_H_ */
