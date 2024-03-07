import machine
from machine import Pin, I2C
from time import sleep
import bmp280
from bmp280_i2c import BMP280I2C

#calibration
temperature_correction = 0; #adjust as needed
pressure_correction = 0;

try:
    #initialize I2C bus
    i2c0_sda = Pin(2)
    i2c0_scl = Pin(3)
    i2c0 = I2C(1, sda=i2c0_sda, scl=i2c0_scl, freq=400000)
    
except Exception as e:
    print("Error found initializing I2C bus: ", e);
    raise SystemExit;

try:
    bmp280_i2c = BMP280I2C(0x77, i2c0) #address might be different, depending on the sensor
except Exception as e:
    print("Error found initializing BMP280 sensor: ",e);
    raise SystemExit;

while True:
    try:
        #read temperature and pressure values
        readout = bmp280_i2c.measurements
        temperature_c = round(readout['t'], 2);
        pressure_hpa = round(readout['p'], 2);
        print(f"Temperature: {temperature_c} °C, Pressure: {pressure_hpa} hPa")
    except Exception as e:
        print("Error found reading sensor (temperature and pressure) data", e);
        raise SystemExit
    finally:
        sleep(1); #delay for 1 sec between readings
    