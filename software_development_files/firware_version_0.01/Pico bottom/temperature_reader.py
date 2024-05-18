from machine import ADC, Pin, I2C
from time import *

class temperature_reader:
    def __init__(self):
        pass  #No need for initialization
    
    def read_temperature(self, temp_sensor_pin):
            """Read temperature from ADC."""
            try:
                temp_adc = ADC(Pin(temp_sensor_pin))
                adc_value = temp_adc.read_u16()
                volt = (3.3 / 65535) * adc_value
                temperature_celsius = (100 * volt) - 50
                return temperature_celsius
            except Exception as e:
                print("Error found reading temperature sensor data/ calculating:", e)
                return None