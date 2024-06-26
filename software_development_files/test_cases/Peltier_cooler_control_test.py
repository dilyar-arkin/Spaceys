from machine import Pin, ADC
import time

def reset_pins():
    gpio_pin_list = range(16, 23) #excluding pin 23
    for i in gpio_pin_list:
        gpio_pin = Pin(i, Pin.OUT)
        gpio_pin.on() #no current
     
reset_pins()
# Define GPIO pins
peltier_pin = Pin(20, Pin.OUT)  # GPIO pin controlling Peltier cooler
temp_sensor_pin = 28            # ADC pin for temperature sensor

# Define ADC object for temperature sensor
#adc.atten(ADC.ATTN_11DB)  # Set attenuation for maximum input voltage of 3.6V

def read_temperature():
    try:
        #Read value from ADC
        temp36 = ADC(28)
        adc_value = temp36.read_u16()
        volt = (3.3/65535)*adc_value
        DegC = (100*volt) - 50
        #print(round(DegC,2))
        return DegC
        
    except Exception as e:
        print("Error found reading sensor data/ calculating");


# Main loop
while True:
    temperature = read_temperature()
    print("Temperature:", temperature, "C")

    if round(temperature) > 40:
        # If temperature exceeds 35 degrees Celsius, turn on Peltier cooler
        peltier_pin.on()
        print("Peltier cooler turned on due to high temperature")
    else:
        # Otherwise, turn on Peltier cooler
        peltier_pin.off()
        

    time.sleep(1)  # Sleep for 1 second before reading temperature again
