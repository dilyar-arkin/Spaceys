from machine import Pin, ADC
import time
import amplifier_controller

class peltier_cooler:    
    def __init__(self, peltier_pin, amp_temp_sensor_pin, heat_sink_temp_sensor_pin, temp_sensor_pin3, temp_sensor_pin4, amplifier):
        self.peltier_pin = PELTIER_PIN
        self.temp_sensor_pin1 = ADC(amp_temp_sensor_pin)
        self.temp_sensor_pin2 = ADC(heat_sink_temp_sensor_pin)
        self.temp_sensor_pin3 = ADC(temp_sensor_pin3)
        self.temp_sensor_pin4 = ADC(temp_sensor_pin4)
        self.amplifier = amplifier  #Store the amplifier instance

    def read_temperature(self, temp_sensor_pin):
        """Read temperature from ADC."""
        try:
            temp_adc = ADC(temp_sensor_pin)
            adc_value = temp_adc.read_u16()
            volt = (3.3 / 65535) * adc_value
            temperature_celsius = (100 * volt) - 50
            return temperature_celsius
        except Exception as e:
            print("Error found reading sensor data/ calculating:", e)
            return None

    def control_peltier(self):
        """Continuously control the Peltier cooler based on temperature values."""
        try:
            while True:
                temperature = self.read_temperature()
                if temperature is not None:
                    self.adjust_peltier(temperature)
                    yield temperature #Yield the temperature value to the caller, without exiting the loop               
                time.sleep(1)  #Sleep for 1 second before reading temperature again
        except KeyboardInterrupt:
            pass  #Exit, if interrupted
    
    def turn_on(self):
        self.peltier_pin.off()
        print("Peltier cooler turned on.")

    def turn_off(self):
        self.peltier_pin.on()
        print("Peltier cooler turned off.")

