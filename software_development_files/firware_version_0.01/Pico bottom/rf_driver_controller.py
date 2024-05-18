from machine import Pin, ADC, I2C
import time

class rf_driver_controller:
    def __init__(self, rf_driver_pin):
        self.rf_driver_pin = RF_DRIVER_PIN

    def turn_on_rf_driver(self):
        self.rf_driver_pin.off()      
        print("RF driver is turned on.")

    def turn_off_rf_driver(self):
        self.rf_driver_pin.on()
        print("RF driver is turned off.")
