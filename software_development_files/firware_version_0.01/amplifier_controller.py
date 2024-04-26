from machine import Pin
import time

#MR amplifier=on, then RF driver=on
#RF driver=off, then MR amplifier=off
class amplifier_controller:
    def __init__(self, mr_amp_pin, rf_drive_pin):
        self.mr_amp_pin = Pin(mr_amp_pin, Pin.OUT)
        self.rf_drive_pin = Pin(rf_drive_pin, Pin.OUT)
        self.on_time = 5  #Default on time
        self.off_time = 5  #Default off time

    def turn_on_mr_amplifier(self):
        self.mr_amp_pin.off()
        print("MR amplifier is turned on.")

    def turn_off_mr_amplifier(self):
        self.mr_amp_pin.on()
        print("MR amplifier is turned off.")

    def turn_on_rf_drive(self):
        self.rf_drive_pin.off()
        print("RF drive is turned on.")

    def turn_off_rf_drive(self):
        self.rf_drive_pin.on()
        print("RF drive is turned off.")
        
    def update_cycle(self, on_time, off_time):
        self.on_time = on_time
        self.off_time = off_time
        print("Updated amplifier cycle: On time =", on_time, "seconds, Off time =", off_time, "seconds.")

