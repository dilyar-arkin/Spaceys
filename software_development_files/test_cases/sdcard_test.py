from sdcard_init_class import *
from machine import ADC
from time import sleep


pico_temp = sdcard_init('pico_temp')

adcpin = 26 # analog to digital convert pin number
temp36 = ADC(4)

try:
    while True:
        adc_value = temp36.read_u16()
        volt = (3.3/65535)*adc_value
        DegC = (100*volt) - 50
        pico_temp.write(str(round(DegC,2)))
        sleep(1)
        print("data saved to sd card")
        
except KeyboardInterrupt:
    print('interrupted!')
        
        
val = pico_temp.read()


print(val)