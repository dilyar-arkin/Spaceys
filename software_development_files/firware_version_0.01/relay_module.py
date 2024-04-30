from machine import Pin, ADC
import time

class relay_module:
    #Define GPIO pins
    pins = [16, 17, 18, 19, 20, 21, 22]

    #Global variable to track the relay failure status
    RELAY_FAILURE = False #Default
    
    @staticmethod #not relying on instance attributes
    def check_relay_failure():
        #Turn on all pins
        for pin_num in pins:
            Pin(pin_num, Pin.OUT).on()
        
        #Delay for a short time
        time.sleep(0.5)
        
        #Turn off all pins
        for pin_num in pins:
            Pin(pin_num, Pin.OUT).off()
        
        #Check if all pins turned on and off simultaneously
        initial_state = [Pin(pin_num).value() for pin_num in pins]
        time.sleep(1)  #Wait for stabilization
        final_state = [Pin(pin_num).value() for pin_num in pins]
        
        #Update RELAY_FAILURE based on its status
        RELAY_FAILURE = initial_state != final_state

    @staticmethod
    def correct_relay_failure():
        pass

    @staticmethod
    def is_relay_failure():
        return RELAY_FAILURE

    @staticmethod
    def reset_relay_failure():
        global RELAY_FAILURE
        RELAY_FAILURE = False

