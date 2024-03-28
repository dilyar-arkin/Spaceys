from machine import Pin, ADC
import time

# Define GPIO pins
counter = 16
peltier_pin = Pin(counter, Pin.OUT)  # GPIO pin controlling Peltier cooler
list = [16,17,18,19,20,21]

while True:
    for index in list:
        peltier_pin = Pin(index, Pin.OUT)  # GPIO pin controlling Peltier cooler
        peltier_pin.on()
        time.sleep(0.5)
        print(index)
        
    for index in list:
        peltier_pin = Pin(index, Pin.OUT)  # GPIO pin controlling Peltier cooler
        peltier_pin.off()
        time.sleep(0.5)
        print(index)
        

