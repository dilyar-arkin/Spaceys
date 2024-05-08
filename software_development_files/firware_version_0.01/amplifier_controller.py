from machine import Pin
import time

#MR amplifier=on, then RF driver=on
#RF driver=off, then MR amplifier=off
class amplifier_controller:
    def __init__(self, mr_amp_pin, rf_drive_pin, amp_temp_sensor_pin):
        self.mr_amp_pin = MR_AMP_PIN
        self.rf_drive_pin = RF_DRIVE_PIN
        self.amp_temp_sensor_pin = AMPLIFIER_TEMP_SENSOR_PIN
        self.on_time = 5  #Default on time
        self.off_time = 5  #Default off time

    def turn_on_amplifiers(self):
        self.mr_amp_pin.off()
        self.rf_drive_pin.off()      
        print("MR amplifier and RF drive are turned on.")

    def turn_off_amplifiers(self):
        self.rf_drive_pin.on()
        self.mr_amp_pin.on()
        print("RF drive and MR amplifier are turned off.")
        
    def update_cycle(self, on_time, off_time):
        self.on_time = on_time
        self.off_time = off_time
        print("Updated amplifier cycle: On time =", on_time, "seconds, Off time =", off_time, "seconds.")
        
    def read_temperature(self):
        """Read temperature from ADC."""
        try:
            temp_adc = ADC(self.amp_temp_sensor_pin)
            adc_value = temp_adc.read_u16()
            volt = (3.3 / 65535) * adc_value
            temperature_celsius = (100 * volt) - 50
            return temperature_celsius
        except Exception as e:
            print("Error found reading sensor data/ calculating:", e)
            return None
        
    def handle_normal_mode(self):
        while True:
            try:
                amplifier_temperature = self.read_temperature()
                heat_sink_temperature = self.read_temperature()
                
                if self.AMBIENT_TEMP_THRESHOLD_LOW <= amplifier_temperature <= self.AMBIENT_TEMP_THRESHOLD_HIGH:
                    #Normal operation
                    self.update_cycle(5, 5)
                    self.turn_on_amplifiers()
                    time.sleep(5)  #Sleep for 5 seconds before checking temperatures again
                else:
                    #Temperature correction mode
                    self.handle_temperature_correction_mode(amplifier_temperature, heat_sink_temperature)
            except KeyboardInterrupt:
                break    
    
    def start_normal_operation(self):
        self.handle_normal_mode()
        print("Normal mode - Amplifier and RF driver on/off cycle (5 sec on / 5 sec off)")
    
