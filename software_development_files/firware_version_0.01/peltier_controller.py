from machine import Pin, ADC
import time

#peltier_pin = Pin(21, Pin.OUT)  #GPIO pin controlling Peltier cooler
#temp_sensor_pin = 28            #ADC pin for temperature sensor

#AMBIENT_TEMP_THRESHOLD_LOW = 0   #Lower temperature threshold for normal operation
#AMBIENT_TEMP_THRESHOLD_HIGH = 40  #Upper temperature threshold for normal operation
#VERY_HIGH_TEMP_THRESHOLD = 80

class peltier_controller:
    def __init__(self, peltier_pin, temp_sensor_pin):
        self.peltier_pin = Pin(peltier_pin, Pin.OUT)
        self.temp_sensor_pin = ADC(temp_sensor_pin)

    def reset_pins(self):
        """Reset GPIO pins."""
        gpio_pin_list = range(16, 23)  #Excluding pin 23
        for i in gpio_pin_list:
            gpio_pin = Pin(i, Pin.OUT)
            gpio_pin.on()  #Pin is actually off, no current

    def read_temperature(self):
        """Read temperature from ADC."""
        try:
            temp_adc = ADC(self.temp_sensor_pin)
            adc_value = temp_adc.read_u16()
            volt = (3.3 / 65535) * adc_value
            temperature_celsius = (100 * volt) - 50
            return temperature_celsius
        except Exception as e:
            print("Error found reading sensor data/ calculating:", e)
            return None

    def control_peltier_cooler(self):
        """Control Peltier cooler based on temperature."""
        try:
            while True:
                temperature = self.read_temperature()
                print("Temperature:", temperature, "C")
                time.sleep(1)  #Sleep for 1 second before reading temperature again
        except KeyboardInterrupt:
            pass  #Exit, if interrupted
    
    def turn_on(self):
        """Turn on the Peltier cooler."""
        self.peltier_pin.off()
        print("Peltier cooler turned on.")

    def turn_off(self):
        """Turn off the Peltier cooler."""
        self.peltier_pin.on()
        print("Peltier cooler turned off.")

