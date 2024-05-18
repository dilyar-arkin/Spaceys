from pico_i2c_lcd import I2cLcd
from machine import I2C, Pin
from utime import sleep

# note: class functionalities are not ready -- need more development -- 20231220- Dilyar
class lcd_display():
    #initialize lcd screen 
    i2c = I2C(0, sda=Pin(0), scl=Pin(1), freq=400000)
    I2C_ADDR = i2c.scan()[0]
    lcd = I2cLcd(i2c, I2C_ADDR, 4, 20)
    # pico microchip temperature sensor readout 
    def picoTemp():
        lcd.clear()
        adcpin = 26 # analog to digital convert pin number
        temp36 = ADC(4) 
        try:
            while True:
                lcd.putstr("pico temperature" + "\n")
                adc_value = temp36.read_u16()
                volt = (3.3/65535)*adc_value
                DegC = (100*volt) - 50
                lcd.putstr(str(round(DegC,2)) + "\n")
                sleep(1)
                lcd.clear()
        except KeyboardInterrupt:
            print('interrupted!')
    
    # bmp sensor readout function
    def bmp_func():
        lcd.clear()
        i2c0_sda = Pin(2)
        i2c0_scl = Pin(3)
        i2c0 = I2C(1, sda=i2c0_sda, scl=i2c0_scl, freq=400000)
        bmp280_i2c = BMP280I2C(0x77, i2c0)  # address may be different
    
        try:       
            while True:
                readout = bmp280_i2c.measurements
                lcd.putstr("Pressure Sensor"+"\n")
                lcd.putstr(f"T: {round(readout['t'],2)} C" +"\n")
                lcd.putstr(f"P: {round(readout['p'],2)} hPa.")
                sleep(1)
                lcd.clear()
                
        except KeyboardInterrupt:
            print('interrupted!')
    
    # 
    def temp_sensor():
        lcd.clear()
        adcpin = 26 # analog to digital convert pin number
        temp36 = ADC(adcpin)
        try:
            while True:
                lcd.clear()
                adc_value = temp36.read_u16()
                volt = (3.3/65535)*adc_value
                DegC = (100*volt) - 53
                lcd.putstr("surface T:" + "\n")
                lcd.putstr(f"            {round(DegC,2)} C")
                sleep(1)
        except KeyboardInterrupt:
            print('interrupted!')
    
    
    # main loop, scan cycle
    while True:
        lcd.clear()
        temp_sensor()
        picoTemp()
        bmp_func()
        #print(I2C_ADDR)
        #lcd.blink_cursor_on()

        #input01 = input()
        lcd.clear()
        #lcd.putstr("you entered: " + input01 )
        #sleep(10)
        #lcd.clear()
        #lcd.putstr("I2C Address:"+str(hex(I2C_ADDR))+"\n")
        lcd.putstr("Spaceys")
        sleep(2)
        #lcd.blink_cursor_off()
        #lcd.clear()
        #lcd.putstr("Backlight Test")
        #sleep(2)
        #lcd.clear()
        for i in range(3):
            lcd.backlight_on()
            lcd.putstr("\n"+"Test")    
            sleep(0.2)
            lcd.backlight_off()
            sleep(0.2)
            
        lcd.backlight_on()
        lcd.hide_cursor()
        lcd.clear()
        #for i in range(20):
        #    lcd.putstr(str(i))
        #    sleep(0.4)
        #    lcd.clear()
