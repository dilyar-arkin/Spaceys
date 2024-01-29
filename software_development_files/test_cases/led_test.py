import machine
from machine import Pin
from time import sleep

led = Pin(25,Pin.OUT)

while True:
    led.on()
    sleep(1.0)
    led.off()
    sleep(1.0)
    print(machine.freq())    
