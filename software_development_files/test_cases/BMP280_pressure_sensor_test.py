from machine import I2C, Pin
from time import sleep
from utime import sleep
from pico_i2c_lcd import I2cLcd
from machine import ADC
import bmp280
from bmp280_configuration import BMP280Configuration
from bmp280_i2c import BMP280I2C

try:
    i2c0_sda = Pin(2)
    i2c0_scl = Pin(3)
    i2c0 = I2C(1, sda=i2c0_sda, scl=i2c0_scl, freq=400000)
except Exception as e:
    print("Error found initializing IC2", e);
    raise SystemExit
try:
    bmp280_i2c = BMP280I2C(0x77, i2c0)  #address may be different
except Exception as e:
    print("Error initializing BMP280 sensor");
    raise SystemExit

while True:
    try:
        readout = bmp280_i2c.measurements
        print(f"T: {round(readout['t'],2)} °C, P: {round(readout['p'],2)} hPa.")
    except Exception as e:
        print("Error found reading sensor data");
        raise SystemExit
    finally:
        sleep(1)
