import machine
from machine import ADC,Pin, I2C
from time import sleep
#from lsm6ds33 import LSM6DS33
import bmp280
from bmp280_i2c import BMP280I2C
from bmp280_configuration import BMP280Configuration
from bmp280_init_class import *
from sdcard_init_class import *

def main():
    try:
        #initialize I2C bus
        i2c1_sda = Pin(2)
        i2c1_scl = Pin(3)
        i2c1 = I2C(1, sda=i2c1_sda, scl=i2c1_scl, freq=400000)
    except Exception as e:
        print("Error found initializing I2C bus: ", e);
        raise SystemExit;

    try:
        bmp280_i2c = BMP280I2C(0x77, i2c1) #address might be different, depending on the sensor
    except Exception as e:
        print("Error found initializing BMP280 sensor: ",e);
        raise SystemExit;
    
    try:
        microSD = sdcard_init('microsd', 13,11,12,10,1)
    except Exception as e:
        print("Error found initializing SD: ", e)
        raise SystemExit

    while True:
        try:
            #read temperature and pressure values
            readout = bmp280_i2c.measurements
            temperature_c = round(readout['t'], 2);
            pressure_hpa = round(readout['p'], 2);
            microSD.write(temperature_c)  

        except Exception as e:
            print("Error found reading sensor (temperature and pressure) data", e);
            raise SystemExit
        finally:
            sleep(1); #delay for 1 sec between readings
    
    #SD = sdcard_init('SD',5,7,4,6,0)
    #BMP_sensor = bmp_func('bmp_sensor')

if __name__ == "__main__":
    main()
