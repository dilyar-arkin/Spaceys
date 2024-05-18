from machine import I2C, Pin
import bmp280
#import bmp280_configuration
#import bmp280_i2c
from bmp280_configuration import BMP280Configuration
from bmp280_i2c import BMP280I2C

class bmp_func():
    name = 'Unknown IO'

    i2c0_sda = Pin(2)
    i2c0_scl = Pin(3)
    i2c0 = I2C(1, sda=i2c0_sda, scl=i2c0_scl, freq=400000)
    bmp280_i2c = BMP280I2C(0x77, i2c0)  # address may be different
    
    def __init__(self,name):
        #Assign I2C comm ports for sda and scl
        self.name = name

    def read(self):
        readout = self.bmp280_i2c.measurements
        return_val = f"T: {round(readout['t'],2)} C " + f"P: {round(readout['p'],2)} hPa"
        return return_val

