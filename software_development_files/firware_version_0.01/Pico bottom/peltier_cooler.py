from machine import ADC, Pin, I2C
from time import sleep

class peltier_cooler:    
    def __init__(self, peltier_pin):
        self.peltier_pin = peltier_pin
    
    def turn_on_peltier(self):
        self.peltier_pin.off()
        print("Peltier cooler turned on.")

    def turn_off_peltier(self):
        self.peltier_pin.on()
        print("Peltier cooler turned off.")