from machine import Pin, ADC
import time

#Define GPIO pins
pins = [16, 17, 18, 19, 20, 21, 22]

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
    time.sleep(1)  # Wait for pins to stabilize
    final_state = [Pin(pin_num).value() for pin_num in pins]
    
    return initial_state == final_state

