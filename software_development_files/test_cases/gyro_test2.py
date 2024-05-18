from machine import ADC, Pin, I2C
from time import sleep
import vector3d
from imu import MPU6050
from MinIMU_v5_pi import *


try:   
    #Initialize IMU
    i2c = I2C(1, sda=Pin(14), scl=Pin(15), freq=400000)
    imu = MPU6050(i2c)
except Exception as e:
    print("Error initializing I2C busses:", e)
    raise SystemExit("I2C bus initialization failed. Exiting program.")

while True:
    ax=round(imu.accel.x,2)
    ay=round(imu.accel.y,2)
    az=round(imu.accel.z,2)
    gx=round(imu.gyro.x)
    gy=round(imu.gyro.y)
    gz=round(imu.gyro.z)
    tem=round(imu.temperature,2)
    print("ax",ax,"\t","ay",ay,"\t","az",az,"\t","gx",gx,"\t","gy",gy,"\t","gz",gz,"\t","Temperature",tem,"        ",end="\r")
    sleep(0.2)