import machine
from machine import ADC,Pin, I2C
import time
import _thread 
#from lsm6ds33 import LSM6DS33
import bmp280
from bmp280_i2c import BMP280I2C
from bmp280_configuration import BMP280Configuration
from bmp280_init_class import *
from sdcard_init_class import *
import amplifier_controller
import peltier_controller
import relay_module

TEMP_SENSOR_PIN = 28  #ADC pin for temperature sensor- amplifier
PELTIER_PIN = Pin(21, Pin.OUT)  #GPIO pin controlling Peltier cooler
MR_AMP_PIN = Pin(16, Pin.OUT)  #GPIO pin controlling MR amplifier
RF_DRIVE_PIN = Pin(17, Pin.OUT)  #GPIO pin controlling RF driver

AMBIENT_TEMP_THRESHOLD_LOW = 0   #Lower temperature threshold for normal operation
AMBIENT_TEMP_THRESHOLD_HIGH = 40  #Upper temperature threshold for normal operation
VERY_HIGH_TEMP_THRESHOLD = 80

def main_thread():
    while True:
        main()
        time.sleep(1)

def relay_thread(): #Continuously checking for relay failure, if detected setting RELAY_FAILURE = true
    while True:
        #Check whether there is relay failure
        relay_module.check_relay_failure()
        time.sleep(1)

def main():     
    #Create instances of amplifier and peltier cooler
    amplifier = amplifier_controller(MR_AMP_PIN, RF_DRIVE_PIN)
    peltier = peltier_cooler(PELTIER_PIN, TEMP_SENSOR_PIN)
    temp_sensor = ADC(TEMP_SENSOR_PIN)
    
    #Reset GPIO pins
    peltier.reset_pins() #Pins 16 to 23, excluding pin 23
    
    try:
        if relay_module.is_relay_failure():
            print("Relay failure detected! Attempting to correct..")
            #Correct the relay module
            relay_module.correct_relay_failure()
            relay_module.reset_relay_failure()
            print("Relay failure corrected. Resuming main cycle.")
        else:
            peltier.control_peltier_cooler() #Read temperature values with 1 second in between
                
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

#Multi-threading
if __name__ == "__main__":
    _thread.start_new_thread(main_thread, ())
    _thread.start_new_thread(relay_thread, ())