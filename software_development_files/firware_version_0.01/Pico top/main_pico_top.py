import machine
from machine import Pin, I2C
from time import sleep
#import os
#import uos
from bmp280_i2c import BMP280I2C
from bmp280_configuration import BMP280Configuration
from bmp280_init_class import *
from sdcard_init_class import *
from temperature_reader import *
from logging import *

"""Define global variables"""
global TEMP_SENSOR3_PIN 
TEMP_SENSOR3_PIN = 27 #ADC pin for temperature sensor 3- microSD
global TEMP_SENSOR4_PIN
TEMP_SENSOR4_PIN = 26 #ADC pin for temperature sensor 4- microSD

"""Configure logging to write to a text file on the Raspberry Pi"""
logger = getLogger()
logger.setLevel(DEBUG)
file_handler = FileHandler("error_log.txt")
file_handler.setLevel(DEBUG)
formatter = Formatter("%(levelname)s:%(name)s:%(message)s")
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

def initialize():
    init_attempts = 0
    microSD = None
    bmp280_i2c = None
    i2c0 = None
    
    while init_attempts < 5:
        all_initialized = True
        try:
            """Initialize microSD card"""
            if not microSD:
                try: 
                    microSD = sdcard_init(13,11,12,10,1)
                except Exception as e:
                    print("Error found initializing microSD: ", e)
                    logger.error("Error found initializing microSD: " + str(e))
                    all_initialized = False
            
            """Initialize I2C bus"""
            if not i2c0:
                try: 
                    i2c0_sda = Pin(2)
                    i2c0_scl = Pin(3)
                    i2c0 = I2C(1, sda=i2c0_sda, scl=i2c0_scl, freq=400000)
                except Exception as e:
                    print("Error found initializing I2C bus: ", e);
                    logger.error("Error found initializing I2C bus: %s" + str(e))
                    all_initialized = False
            
            """Initialize BMP280 sensor"""
            if not bmp280_i2c and i2c0:
                try: 
                    bmp280_i2c = BMP280I2C(0x77, i2c0)
                except Exception as e:
                    print("Error found initializing BMP280 sensor: ",e);
                    logger.error("Error found initializing BMP280 sensor: " + str(e))
                    all_initialized = False
                
            if all_initialized:
                return microSD, i2c0, bmp280_i2c
            
        except Exception as e:
            print(f"Unexpected error during initialization: {e}")
            logger.error(f"Unexpected error during initialization: {e}")
            
        init_attempts += 1
        print(f"Initialization attempt {init_attempts} failed. Retrying...")
        logger.error(f"Initialization attempt {init_attempts} failed.")
        sleep(1)  # Wait before retrying
        
    print(f"Failed to initialize after {init_attempts} attempts but proceeded with returned values if any.")
    logger.error(f"Failed to initialize after {init_attempts} attempts but proceeded with returned values if any.")
    return microSD, i2c0, bmp280_i2c
            
def main():
    
    microSD, i2c0, bmp280_i2c = initialize()
    
    #Create an instance of temperature_reader for each temperature sensor
    temperature_sensor = temperature_reader()

    while True:
        """Read and save BMP280 data"""
        if bmp280_i2c is not None and microSD is None:
            raise SystemExit
        if bmp280_i2c is not None: #If BMP280 sensor and microSD are both initialized
            try:
                #Read temperature and pressure values from BMP280 sensor
                readout = bmp280_i2c.measurements
                temperature_c = round(readout['t'], 2);
                pressure_hpa = round(readout['p'], 2);
                #Write BMP280 temperature and pressure data to different text files
                microSD.write("BMP280 Sensor-Temperature", temperature_c)
                microSD.write("BMP280 Sensor-Pressure", pressure_hpa)
            except Exception as e:
                print("Error found reading and/or writing BMP 280 sensor (temperature and pressure) data", e);
                logger.error("Error found reading and/or writing BMP280 sensor (temperature and pressure) data: " + str(e))
            finally:
                sleep(1); #Delay for 1 sec between readings
        
        """Read and save temperature values from temp. sensors 3 and 4"""
        if microSD is not None: #If microSD card is initialized
            try:
                #Read temperature values from temperature sensors attached to microSD
                temperature_sensor3_data = temperature_sensor.read_temperature(TEMP_SENSOR3_PIN)
                temperature_sensor4_data = temperature_sensor.read_temperature(TEMP_SENSOR4_PIN)
                #Write temperature data to text files in microSD card
                if temperature_sensor3_data is not None:
                    microSD.write("Temperature Sensor 3-Data", temperature_sensor3_data)
                if temperature_sensor4_data is not None:
                    microSD.write("Temperature Sensor 4-Data", temperature_sensor4_data)
            except Exception as e:
                print("Error found reading and/or writing temperature data from temperature sensor 3 and 4 (connected to microSD)", e)
                logger.error("Error found reading and/or writing temperature data from temperature sensor 3 and 4 (connected to microSD): " + str(e))
            finally:
                sleep(1) #Delay for 1 sec between readings  
        else:
            raise SystemExit

if __name__ == "__main__":
    main()

