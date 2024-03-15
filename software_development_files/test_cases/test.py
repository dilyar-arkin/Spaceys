import machine
from machine import Pin, I2C
import time
from time import sleep


pin_led= Pin(22, mode= Pin.OUT) #connected to relay

while True:
    time.sleep(10)
    pin_led.toggle()
    time.sleep(5)




    
