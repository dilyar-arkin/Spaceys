from machine import I2C, Pin
import time
from time import sleep
from utime import sleep
from pico_i2c_lcd import I2cLcd
from machine import ADC
import bmp280
from bmp280_configuration import BMP280Configuration
from bmp280_i2c import BMP280I2C


threshold_temperature_high = 30 
threshold_temperature_low = 10   

def read_temperature(sensor):
    return sensor.measurements['t']

def activate_cooler():

    pass

def deactivate_cooler():
 
    pass

high_temp = False
low_temp = False

while True:
    try:
        i2c0_sda = Pin(2)
        i2c0_scl = Pin(3)
        i2c0 = I2C(1, sda=i2c0_sda, scl=i2c0_scl, freq=400000)
    except Exception as e:
        print("Error found initializing I2C bus:", e)
        raise SystemExit
    
    try:
        bmp280_i2c = BMP280I2C(0x77, i2c0) #address may be different
    except Exception as e:
        print("Error initializing BMP280 sensor:", e)
        raise SystemExit

    try:
        temperature = read_temperature(bmp280_i2c)
        print(f"T: {round(temperature,2)} °C")
        
        if temperature > threshold_temperature_high:
            high_temp = True
            low_temp = False
        elif temperature < threshold_temperature_low:
            high_temp = False
            low_temp = True
        else:
            high_temp = False
            low_temp = False
            
        if high_temp or low_temp:
            activate_cooler()
        else:
            deactivate_cooler()
            
    except Exception as e:
        print("Error found:", e)
        raise SystemExit
    finally:
        utime_sleep(1)
