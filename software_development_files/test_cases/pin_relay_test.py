from machine import Pin
import time

def reset_pins():
    gpio_pin_list = range(16, 23) #excluding pin 23
    for i in gpio_pin_list:
        gpio_pin = Pin(i, Pin.OUT)
        gpio_pin.on()
   
reset_pins()
current_pin = Pin(21, Pin.OUT)

while True:
    current_pin.off() #pin is actually on, current goes through
    print("pin on")
    time.sleep(2)
    current_pin.on() #pin is actually off, no current
    print("pin off")
    time.sleep(2)