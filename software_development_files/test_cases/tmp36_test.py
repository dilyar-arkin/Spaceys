from machine import ADC
from time import sleep
from machine import I2C

# Initialize and Read values from TMP36 temperature sensor 
adcpin = 26 # analog to digital convert pin number
temp36 = ADC(4) 
con = 1 

while con != 0:
    try:
        #Read value from ADC
        adc_value = temp36.read_u16()
        volt = (3.3/65535)*adc_value
        DegC = (100*volt) - 50
        print(round(DegC,2))
        sleep(1)
        if round(DegC,2) > 38:
            con = 0
    except Exception as e:
        print("Error found reading sensor data/ calculating");


