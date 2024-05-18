from machine import ADC, Pin, I2C
from time import *

#K2 and K3 are shorted due to soldering. They turn on and off at the same time.

class relay_module:
    #Define GPIO pins for the relay module
    pins = [16, 17, 18, 19, 20, 21, 22]

    #Global variable to track the relay failure status
    RELAY_FAILURE = False #Default
    
    @staticmethod #not relying on instance attributes
    def check_relay_failure():
        try:
            #Turn on all pins
            for pin_num in relay_module.pins:
                gpio_pin = Pin(pin_num, Pin.OUT)
                gpio_pin.off() #Pin is actually on, current goes through (opposite true)
                
            #Delay for a short time
            time.sleep(0.5)
            
            #Turn off/ Reset pins to off state
            for pin_num in relay_module.pins:
                gpio_pin = Pin(pin_num, Pin.OUT)
                gpio_pin.on() #Pin is actually off, no current
            
            #Check if all pins turned on and off simultaneously
            initial_state = [Pin(pin_num).value() for pin_num in relay_module.pins]
            time.sleep(1)  #Wait for stabilization
            final_state = [Pin(pin_num).value() for pin_num in relay_module.pins]
            
            #Update RELAY_FAILURE based on its status
            RELAY_FAILURE = initial_state != final_state
            
        except Exception as e:
            print("Error in relay resetting:", e)
            relay_module.RELAY_FAILURE = True

    @staticmethod
    def is_relay_failure():
        return relay_module.RELAY_FAILURE

    @staticmethod
    def correct_relay_failure(): #Corrective action to take place if RELAY_FAILURE is True
        print("Relay failure detected! Attempting to correct..")
        relay_module.check_relay_failure() #Reset pins
        machine.reset() #Soft reset of the microcontroller
        relay_module.RELAY_FAILURE = False
        print("Relay failure corrected. Resuming main cycle.")
        pass
            