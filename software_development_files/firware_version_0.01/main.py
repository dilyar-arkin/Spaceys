#from sdcard_init_class import *
#from bmp280_init_class import *
from machine import ADC
from time import sleep
from machine import Pin,I2C
from lsm6ds33 import LSM6DS33
import bmp280
from bmp280_configuration import BMP280Configuration
from bmp280_i2c import BMP280I2C


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


#i2c1_sda = Pin(18)
#i2c1_scl = Pin(19)
#i2c1 = I2C(1, sda=i2c1_sda, scl=i2c1_scl, freq=400000)
    
#gyr = LSM6DS33(i2c1)
#gyr.a()
#gyr.g()

#classes
class Pressure:
    def __init__(self):
        pass

class Temperature:
    def __init__(self):
        pass

    def initialize_pins(self):
        pass 

class Gyro:
    def __init__(self):
        pass

def read_data():
    pass 

def save_data():
    pass

def RFtransmit():
    pass

def check_temp():
    pass

def PID(temperature_sensors):
    pass

def activate_cooler():
    print("Peltier cooler activated.")

def deactivate_cooler():
    print("Peltier cooler deactivated.")

def main():
    #initialize I2C bus
    try: 
        i2c0_sda = Pin(2)
        i2c0_scl = Pin(3)
        i2c0 = I2C(1, sda=i2c0_sda, scl=i2c0_scl, freq=400000)
    except Exception as e:
        print("Error found initializing I2C bus:", e);
        raise SystemExit;
    
    #initialize BMP280 sensor
    try:
        bmp280_i2c = BMP280I2C(0x77, i2c0) #address might be different, depending on the sensor
    except Exception as e:
        print("Error found initializing BMP280 sensor: ",e);
        raise SystemExit;

    #create instance of Pressure class
    pressure = Pressure()
    #create instances of Temperature() class
    temperature_array = [Temperature() for _ in range(5)]  #for 5 temperature sensors
    for temp in temperature_array:
        temp.initialize_pins() #calling initialize_pins() method on each element of temperature_array
    #create instance of Gyro() class
    gyro = Gyro()

    safety = True
    temp_high = False
    #read and write data
    #implement safety protocols
    while safety:
        read_data()
        save_data()
        RFtransmit()
        check_temp()
        if temp_high:
            PID(temperature_array)
            if temp_tooHigh:
                RFtransmit() #stop transmission
                sleep(1)  #add delay to ensure transmission completes
                Turn_off_power() 
                safety = False
                break

        #check temperature to see whether to activate Peltier cooler or not
        high_temp = False
        low_temp = False

        for sensor in temperature_sensors:
            temperature = read_temperature(sensor)
            if temperature > threshold_temperature_high:
                high_temp = True
                break
            elif temperature < threshold_temperature_low:
                low_temp = True
                break
            
        if high_temp:
            activate_cooler()
        elif low_temp:
            activate_cooler()
        else:
            deactivate_cooler()

        #read BMP280 values
        try:
            readout = bmp280_i2c.measurements
            temperature_c = round(readout['t'], 2);
            pressure_hpa = round(readout['p'], 2);
            print(f"Temperature: {temperature_c} °C, Pressure: {pressure_hpa} hPa")
        except Exception as e:
            print("Error found reading sensor (temperature and pressure) data", e);
            raise SystemExit
        finally:
            sleep(1); #delay for 1 sec between readings
            
    try:
        pass
    except Exception as e:
        print("An error occurred:", e)

if __name__ == "__main__":
    main()

