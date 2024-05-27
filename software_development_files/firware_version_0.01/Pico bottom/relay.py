from machine import ADC, Pin, I2C
import time

#K2 and K3 are shorted due to soldering. They turn on and off at the same time.

class relay:
    #Define GPIO pins for the relay module
    pins = [16, 17, 18, 19, 20, 21, 22]

    #Global variable to track the relay failure status
    RELAY_FAILURE = False #Default
    
    """@staticmethod #not relying on instance attributes
    async def check_relay_failure():
        try:
            #Turn on all pins
            for pin_num in relay.pins:
                gpio_pin = Pin(pin_num, Pin.OUT)
                gpio_pin.off() #Pin is actually on, current goes through (opposite true)
                
            #Delay for a short time
            time.sleep(0.5)
            
            #Turn off/ Reset pins to off state
            for pin_num in relay.pins:
                gpio_pin = Pin(pin_num, Pin.OUT)
                gpio_pin.on() #Pin is actually off, no current
            
            #Check if all pins turned on and off simultaneously
            initial_state = [Pin(pin_num).value() for pin_num in relay.pins]
            time.sleep(1)  # Wait for stabilization
            final_state = [Pin(pin_num).value() for pin_num in relay.pins]
            
            #Update RELAY_FAILURE based on its status
            RELAY_FAILURE = initial_state != final_state
            
            #If relay is all good, print a message to the console
            if not relay.RELAY_FAILURE:
                print("Relay is functioning properly.")
            
        except Exception as e:
            print("Error in relay resetting:", e)
            relay.RELAY_FAILURE = True"""
    
    #This method will initialize the RELAY_FAILURE variable based on a simple read/ without toggling the pins due to PLL
    def initialize_relay_failure_status():
        initial_state = [Pin(pin_num).value() for pin_num in relay.pins]
        time.sleep(1)  # Simulate waiting for stabilization
        final_state = [Pin(pin_num).value() for pin_num in relay.pins]
    
        relay.RELAY_FAILURE = initial_state != final_state
    
    @staticmethod
    def is_relay_failure():
        return relay.RELAY_FAILURE

    """@staticmethod
    async def correct_relay_failure(): #Corrective action to take place if RELAY_FAILURE is True
        print("Relay failure detected! Attempting to correct..")
        await relay.check_relay_failure()  # Reset pins
        machine.reset() #Soft reset of the microcontroller
        relay.RELAY_FAILURE = False
        print("Relay failure corrected. Resuming main cycle.")
        pass"""
    