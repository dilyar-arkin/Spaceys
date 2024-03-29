from machine import Pin
import time
#MR amplifier=on, then RF driver=on
#RF driver=off, then MR amplifier=off

gpio_pin_list = range(16, 23) #excluding pin 23
for i in gpio_pin_list:
    gpio_pin = Pin(i, Pin.OUT)
    gpio_pin.on() #no current
    
# Define GPIO pins
mr_amp_pin = Pin(16, Pin.OUT)    
rf_drive_pin = Pin(17, Pin.OUT) 

def turn_on_mr_amplifier():
    mr_amp_pin.off()
    print("MR amplifier is turned on.")

def turn_off_mr_amplifier():
    mr_amp_pin.on()
    print("MR amplifier is turned off.")

def turn_on_rf_drive():
    rf_drive_pin.off()
    print("RF drive is turned on.")

def turn_off_rf_drive():
    rf_drive_pin.on()
    print("RF drive is turned off.")

while True:
    # MR amplifier is on first:
    turn_on_mr_amplifier()
    time.sleep(1)  

    # RF drive is on after MR amplifier:
    turn_on_rf_drive()
    time.sleep(1)  

    # RF drive is off before MR amplifier:
    turn_off_rf_drive()
    time.sleep(1)  

    # MR amplifier is off later:
    turn_off_mr_amplifier()
    time.sleep(1)  
