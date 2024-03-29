from machine import Pin, ADC
import time

#K2 and K3 are shorted due to soldering. They turn on and off at the same time. 

# Define GPIO pins
counter = 16
peltier_pin = Pin(counter, Pin.OUT)  # GPIO pin controlling Peltier cooler
list = [16,17,18,19,20,21,22]

while True:
    for index in list:
        peltier_pin = Pin(index, Pin.OUT)  # GPIO pin controlling Peltier cooler
        peltier_pin.on()
        time.sleep(2)
        print(index)
        
    for index in list:
        peltier_pin = Pin(index, Pin.OUT)  # GPIO pin controlling Peltier cooler
        peltier_pin.off()
        time.sleep(2)
        print(index)
        

