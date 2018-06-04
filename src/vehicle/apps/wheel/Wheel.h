/*
 * Wheel.h
 *
 *  Created on: Feb 23, 2018
 *      Author: thagen
 */

#ifndef SRC_SEB_VEHICLE_APPS_ENGINE_WHEEL_H_
#define SRC_SEB_VEHICLE_APPS_ENGINE_WHEEL_H_

class Wheel
{
public:
    Wheel(int size);
    virtual ~Wheel();

    virtual int getSize();

private:
    int m_size;
};

#endif /* SRC_SEB_VEHICLE_APPS_ENGINE_WHEEL_H_ */
