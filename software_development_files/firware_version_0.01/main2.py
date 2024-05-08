from machine import ADC,Pin, I2C
import time
import _thread 

import pico_i2c_lcd
import lcd_api
import lcd_display_init_class

import bmp280
from bmp280_i2c import BMP280I2C
from bmp280_configuration import BMP280Configuration
import bmp280_init_class

import sdcard_init_class
import sdcard

import vector3d
import imu
import MinIMU_v5_pi

import relay_module
import amplifier_controller
import peltier_cooler
import PID_controller

#Define GPIO pins
global AMPLIFIER_TEMP_SENSOR_PIN = 28  #ADC pin for amplifier temperature sensor
global HEAT_SINK_TEMP_SENSOR_PIN =     #ADC pin for heat sink temperature sensor
global TEMP_SENSOR3 =    #ADC pin for temperature sensor 3
global TEMP_SENSOR4 =    #ADC pin for temperature sensor 4
global PELTIER_PIN = Pin(21, Pin.OUT)  #GPIO pin controlling Peltier cooler
global MR_AMP_PIN = Pin(16, Pin.OUT)  #GPIO pin controlling MR amplifier
global RF_DRIVE_PIN = Pin(17, Pin.OUT)  #GPIO pin controlling RF driver

#Main thread function
def main_thread():
    while True:
        main()
        time.sleep(1)
       
#Relay thread function
"""Continuously checking for relay failure, if detected setting RELAY_FAILURE = true"""
def relay_thread(): 
    while True:
        try:
            relay_module.check_relay_failure()
            """lock to safely access and modify (shared variable) RELAY_FAILURE; prevent race conditions and inconsistency"""
            with relay_lock: 
                if relay_module.is_relay_failure(): 
                    relay_module.correct_relay_failure() #Correct the relay module, if there is failure/ (if true)
        except RuntimeError as e:
            print("Thread-specific error occurred:", e) 
        except Exception as e:
            print("Error in relay thread:", e)
        time.sleep(1)

def main():
    #Create instances of amplifiers and peltier cooler
    amplifier = amplifier_controller(MR_AMP_PIN, RF_DRIVE_PIN)
    peltier = peltier_cooler(PELTIER_PIN, AMPLIFIER_TEMP_SENSOR_PIN, HEAT_SINK_TEMP_SENSOR_PIN, TEMP_SENSOR3, TEMP_SENSOR4, amplifier)
    
    #Initialization
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
        microSD = sdcard_init('microsd', 13,11,12,10,1)
        SD = sdcard_init('SD',5,7,4,6,0)
    except Exception as e:
        print("Error found initializing SD cards: ", e)
        raise SystemExit
    
    #Setup the MinIMU_v5_pi
    IMU = MinIMU_v5_pi()
    #Initiate tracking of Yaw on the IMU
    IMU.trackYaw()
    
    #Reset GPIO pins
    peltier.reset_pins() #Pins 16 to 23, excluding pin 23
    
    try:
        if relay_module.is_relay_failure():
            relay_module.correct_relay_failure() #Correct the relay module, if there is failure
        else:
            """Read and save temperature values, check for the temperature correction mode to be activated. """
            peltier.control_peltier() #If no relay failure, proceed and read temperature values with 1 second in between and save to SD, checks conditions for temperature correction mode    
                  
            #Normal Mode
            amplifier.start_operation()

    except KeyboardInterrupt:
        print("Exiting program")
        return #Exit the main() function
        
    except Exception as e:
        print("Error: ", e)
        return #Exit the main() function

if __name__ == "__main__":
    try:
        #Lock to synchronize access to RELAY_FAILURE
        relay_lock = _thread.allocate_lock()

        #Start the relay thread
        _thread.start_new_thread(relay_thread, ())

        #Start the main thread
        _thread.start_new_thread(main_thread, ())
    except RuntimeError as e:
        print("Thread-specific error occurred during thread creation:", e) 
    except Exception as e:
        print("Error occurred during thread creation:", e)
