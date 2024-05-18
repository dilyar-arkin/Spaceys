from machine import ADC, Pin, I2C
from time import *
#import os
#import uos
import asyncio
from sdcard_init_class import sdcard_init
from sdcard import SDCard
from imu import MPU6050
from  temperature_reader import *
from relay import *
from rf_driver_controller import *
from peltier_cooler import *

"""Define global variables"""
global RF_DRIVER_TEMP_SENSOR_PIN
RF_DRIVER_TEMP_SENSOR_PIN = 27 #ADC pin for RF driver temperature sensor- data saved to SD
global TEMP_SENSOR2_PIN
TEMP_SENSOR2_PIN = 28 #ADC pin for temperature sensor connected to Peltier cooler- data saved to SD
global PELTIER_PIN
PELTIER_PIN = Pin(20, Pin.OUT) #GPIO pin controlling Peltier cooler
global RF_DRIVER_PIN
RF_DRIVER_PIN = Pin(17, Pin.OUT) #GPIO pin controlling RF driver

async def initialize():
    
    
    """Initialize SD card (bigger)"""
    try:
        SD = sdcard_init(5,7,4,6,0)
    except Exception as e:
        print("Error found initializing SD (bigger): ", e)
        raise SystemExit
    
    """Initialize I2C bus"""
    try:
        i2c0_sda = Pin(14)
        i2c0_scl = Pin(15)
        i2c0 = I2C(1, sda=i2c0_sda, scl=i2c0_scl, freq=400000)
    except Exception as e:
        print("Error found initializing I2C bus: ", e);
        raise SystemExit;
    
    """Initialize IMU"""
    try:
        imu = MPU6050(i2c0)
    except Exception as e:
        print("Error initializing IMU:", e)
        raise SystemExit("IMU initialization failed. Exiting program.")
    
    #Create instances of RF driver and Peltier cooler
    rf_driver = rf_driver_controller(RF_DRIVER_PIN)
    peltier = peltier_cooler(PELTIER_PIN)
    #Create an instance of temperature_reader for temperature sensor 2 and RF driver's temperature sensor
    temperature_sensor = temperature_reader()
    
    return SD, i2c0, imu, rf_driver, peltier, temperature_sensor

async def rf_driver_temperature_check(SD, rf_driver, peltier, temperature_sensor):
    """Check RF driver temperature and adjust Peltier cooler if necessary"""
    while True:
        try:
            #Read RF driver temperature
            rf_driver_temp_data = temperature_sensor.read_temperature(RF_DRIVER_TEMP_SENSOR_PIN)
            #Temperature condition check- control Peltier cooler based on RF driver's temperature
            if 40 < rf_driver_temp_data < 80:
                peltier.turn_on_peltier()
            elif rf_driver_temp_data > 80:
                rf_driver.turn_off_rf_driver()
            #Write RF driver's temperature data to SD card
            if rf_driver_temp_data is not None:
                SD.write("RF Driver Temperature", rf_driver_temp_data)
        except Exception as e:
            print("Error occurred during temperature condition check and adjusting Peltier cooler and/or turning off RF driver:", e)
            raise SystemExit
        await asyncio.sleep(1)

async def temperature_sensor_reading(SD, temperature_sensor):
    """Read data from temperature sensor 2 (connected to Peltier cooler)"""
    while True:
        try:
            #Read temperature values from temperature sensor 2 attached to SD (bigger) and connected to Peltier
            temperature_sensor2_data = temperature_sensor.read_temperature(TEMP_SENSOR2_PIN)
            #Write temperature data to text file in SD card
            if temperature_sensor2_data is not None:
                SD.write("Temperature Sensor 2-(Peltier)-Data", temperature_sensor2_data)
        except Exception as e:
            print("Error found reading and/or writing temperature data from temperature sensor 2 connected to Peltier cooler (saved to SD)", e)
            raise SystemExit
        await asyncio.sleep(1)
              
async def gyroscope_reading(SD, imu):
    """Read and save gyroscope data"""
    while True:
        try:
            #Read gyroscope values
            gx = round(imu.gyro.x)
            gy = round(imu.gyro.y)
            gz = round(imu.gyro.z)
            tem = round(imu.temperature, 2)        
            #Write gyroscope data to SD card
            SD.write("Gyroscope_Data", f"GX: {gx}, GY: {gy}, GZ: {gz}, Temperature: {tem}")
        except Exception as e:
            print("Error occurred during gyroscope data reading and/or writing to SD card:", e)
            raise SystemExit
        await asyncio.sleep(1)

async def main():
    SD, i2c0, imu, rf_driver, peltier, temperature_sensor = await initialize()
    
    #Turn on RF driver in the beginnging
    rf_driver.turn_on_rf_driver()  #RF driver runs continuously - 1 Watt
    
    tasks = [
        rf_driver_temperature_check(SD, rf_driver, peltier, temperature_sensor),
        temperature_sensor_reading(SD, temperature_sensor),
        gyroscope_reading(SD, imu)
    ]
    await asyncio.gather(*tasks)
    
if __name__ == "__main__":
    asyncio.run(main())
