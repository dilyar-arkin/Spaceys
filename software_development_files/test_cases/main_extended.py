import machine
from machine import Pin, I2C
from time import sleep
import bmp280
from bmp280_i2c import BMP280I2C
import time
import calibration

#calibration
temperature_correction = 0; 
pressure_correction = 0;

temperature_sensors = ["Sensor1", "Sensor2", "Sensor3", "Sensor4", "Sensor5"]
pressure_sensors = ["Sensor1", "Sensor2", "Sensor3", "Sensor4", "Sensor5"]

#define threshold values
threshold_temperature_high = 30 #Celcius
threshold_temperature_low = -30 #Celcius
threshold_pressure = 1000 #hPa

def activate_cooler():
    print("Peltier cooler activated.")
    
def deactivate_cooler():
    print("Peltier cooler deactivated.")

def main():
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
    
    while(True):
        high_temp = false 
        low_temp = false
        
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
    