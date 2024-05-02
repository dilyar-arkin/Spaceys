from machine import ADC,Pin, I2C
import time
import _thread 

import pico_i2c_lcd
import lcd_api
import lcd_display_init_class

import bmp280
from bmp280_i2c import BMP280I2C
from bmp280_configuration import BMP280Configuration
from bmp280_init_class import *

from sdcard_init_class import *
import sdcard

import vector3d
import imu
from MinIMU_v5_pi import MinIMU_v5_pi

import amplifier_controller
import peltier_cooler
import relay_module
import PID_controller

#Define GPIO pins
TEMP_SENSOR_PIN1 = 28  #ADC pin for temperature sensor1
TEMP_SENSOR_PIN2 = 
TEMP_SENSOR_PIN3 = 
TEMP_SENSOR_PIN4 = 
PELTIER_PIN = Pin(21, Pin.OUT)  #GPIO pin controlling Peltier cooler
MR_AMP_PIN = Pin(16, Pin.OUT)  #GPIO pin controlling MR amplifier
RF_DRIVE_PIN = Pin(17, Pin.OUT)  #GPIO pin controlling RF driver

#Define temperature thresholds
AMBIENT_TEMP_THRESHOLD_LOW = 0   #Lower temperature threshold for normal operation
AMBIENT_TEMP_THRESHOLD_HIGH = 40  #Upper temperature threshold for normal operation
VERY_HIGH_TEMP_THRESHOLD = 80 #Extreme temperature

#Main thread function
def main_thread():
    while True:
        main()
        time.sleep(1)
       
#Relay thread function
def relay_thread(): #Continuously checking for relay failure, if detected setting RELAY_FAILURE = true
    while True:
        try:
            relay_module.check_relay_failure()
            with relay_lock: #lock to safely access and modify (shared variable) RELAY_FAILURE; prevent race conditions and inconsistency
                if relay_module.is_relay_failure(): 
                    relay_module.correct_relay_failure() #Correct the relay module, if there is failure (if true)
        except RuntimeError as e:
            print("Thread-specific error occurred:", e) 
        except Exception as e:
            print("Error in relay thread:", e)
        time.sleep(1)

def main():     
    #Create instances of amplifiers and peltier cooler
    amplifier = amplifier_controller(MR_AMP_PIN, RF_DRIVE_PIN)
    peltier = peltier_cooler(PELTIER_PIN, TEMP_SENSOR_PIN)
    temp_sensor = ADC(TEMP_SENSOR_PIN)
    
    #Reset GPIO pins
    peltier.reset_pins() #Pins 16 to 23, excluding pin 23
    
    try:
        if relay_module.is_relay_failure():
            relay_module.correct_relay_failure() #Correct the relay module, if there is failure
        else:
            peltier.control_peltier_cooler() #If no relay failure, proceed and read temperature values with 1 second in between
                
            #Temperature correction mode
            if AMBIENT_TEMP_THRESHOLD_HIGH < temperature < VERY_HIGH_TEMP_THRESHOLD:
                print("High temperature detected, changing on/off cycle to 10 sec on / 10 sec off")
                amplifier.update_cycle(10, 10)  #10 sec on / 10 sec off
            elif temperature > VERY_HIGH_TEMP_THRESHOLD:
                print("Very high temperature detected, turning off amplifier and turning on Peltier cooler until temperature is smaller than 40 degrees Celcius")
                amplifier.turn_off_mr_amplifier() 
                peltier.turn_on()
            elif temperature < AMBIENT_TEMP_THRESHOLD_HIGH:
                print("Temperature is lower than 40 degrees Celsius but heat sink is cold, turning off Peltier cooler and changing on/off cycle to 10 sec on /  5 sec off")
                amplifier.update_cycle(10, 5) #10 sec on / 5 sec off
                peltier.turn_off()
            else:
                print("Temperature within normal range, resetting to default cycle")
                amplifier.update_cycle(5, 5)
                  
            #Normal Mode
            print("Normal mode - Amplifier and RF driver on/off cycle (5 sec on / 5 sec off)")
            amplifier.turn_on_mr_amplifier()
            amplifier.turn_on_rf_drive()
            amplifier.turn_off_rf_drive()
            amplifier.turn_off_mr_amplifier()
            
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

        # Start the main thread
        _thread.start_new_thread(main_thread, ())
    except RuntimeError as e:
        print("Thread-specific error occurred during thread creation:", e) 
    except Exception as e:
        print("Error occurred during thread creation:", e)
