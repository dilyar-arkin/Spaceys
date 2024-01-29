#from sdcard_init_class import *
#from bmp280_init_class import *
from machine import ADC
from time import sleep
from machine import Pin,I2C
from lsm6ds33 import LSM6DS33


#instantiate objects corresponds to sensors
# pressure sensor object named bmp_sensor
#BMP_sensor = bmp_func('bmp_sensor')
# sd card object writes to and reads from bmp_sensor_vals.txt
#microsd = sdcard_init('microSD',5,7,4,6,0)
#BMP_sd2 = sdcard_init('bmp_sensor_vals',13,11,12,10,1)
#bmp_sdio = sdFileAccess('bmp280_data')
#pico_sdio = sdFileAccess('pico_temperature_data')

#------------------
#writes BMP280 sensor measurement values to file on sdcard
#bmp_sdio.write(BMP_sensor.read())



#adcpin = 26 # analog to digital convert pin number
#temp36 = ADC(4) 
#adc_value = temp36.read_u16()
#volt = (3.3/65535)*adc_value
#DegC = (100*volt) - 50


#pico_sdio.write(round(DegC,2))


i2c1_sda = Pin(18)
i2c1_scl = Pin(19)
i2c1 = I2C(1, sda=i2c1_sda, scl=i2c1_scl, freq=400000)
    
gyr = LSM6DS33(i2c1)
gyr.a()
gyr.g()

