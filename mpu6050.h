/*
 * mpu6050.h
 *
 *  Created on: Jun 12, 2026
 *      Author: Jason
 */

#ifndef INC_MPU6050_H_
#define INC_MPU6050_H_



#endif /* INC_MPU6050_H_ */


#include <stdint.h>
#include "main.h"

// MPU6050 structure
typedef struct
{

    int16_t Accel_X_RAW;
    int16_t Accel_Y_RAW;
    int16_t Accel_Z_RAW;
    double Ax;
    double Ay;
    double Az;

    int16_t Gyro_X_RAW;
    int16_t Gyro_Y_RAW;
    int16_t Gyro_Z_RAW;
    double Gx;
    double Gy;
    double Gz;

    double AccelAngleX;
    double AccelAngleY;

    double AccelAngleX_2;

    double GyroAngleX;
    double GyroAngleY;
    double GyroAngleZ;

    double CompFiltX;
    double CompFiltY;

    double x;
    double dt;


    float Temperature;

} MPU6050_t;

uint8_t MPU6050_Init(I2C_HandleTypeDef *I2Cx);

void MPU6050_Set_Freq_Hz(int freq, MPU6050_t *DataStruct);

void MPU6050_Set_X(double x, MPU6050_t *DataStruct);

void MPU6050_Read_Accel(I2C_HandleTypeDef *I2Cx, MPU6050_t *DataStruct);

void MPU6050_Read_Gyro(I2C_HandleTypeDef *I2Cx, MPU6050_t *DataStruct);

void MPU6050_Read_Temp(I2C_HandleTypeDef *I2Cx, MPU6050_t *DataStruct);

void MPU6050_Read_All(I2C_HandleTypeDef *I2Cx, MPU6050_t *DataStruct);
