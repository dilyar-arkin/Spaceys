from machine import Pin, ADC
import time
import amplifier_controller
import peltier_cooler

class modes:
    #Define temperature thresholds
    AMBIENT_TEMP_THRESHOLD_LOW = 0   #Lower temperature threshold for normal operation
    AMBIENT_TEMP_THRESHOLD_HIGH = 40  #Upper temperature threshold for normal operation
    VERY_HIGH_TEMP_THRESHOLD = 80 #Extreme temperature
    
    def temperature_correction_mode(self, amp_temperature, heat_sink_temperature, amplifier, peltier):
        try:
            if self.amplifier|| self.peltier is None:
                raise ValueError("Amplifier/ Peltier instance is/ are not provided.")
            
            if self.AMBIENT_TEMP_THRESHOLD_HIGH < amp_temperature < self.VERY_HIGH_TEMP_THRESHOLD:
                print("High temperature detected, changing on/off cycle to 10 sec on / 10 sec off and turning on Peltier cooler is smaller than 40 degrees Celcius")
                amplifier.update_cycle(10, 10)  #10 sec on / 10 sec off cycle
                amplifier.turn_on_amplifiers()  # Turn amplifiers on
                peltier.turn_on() #Turn Peltier cooler on
            elif amp_temperature > self.VERY_HIGH_TEMP_THRESHOLD:
                print("Very high temperature detected, turning off amplifier and turning on Peltier cooler until temperature is smaller than 40 degrees Celcius")
                amplifier.turn_off_amplifiers() #Turn off amplifiers
                peltier.turn_on() #Turn Peltier cooler on
            elif amp_temperature < self.AMBIENT_TEMP_THRESHOLD_HIGH && heat_sink_temperature< AMBIENT_TEMP_THRESHOLD_LOW:
                print("Temperature is lower than 40 degrees Celsius but heat sink is cold, changing on/off cycle to 10 sec on /  5 sec off and turning of Peltier cooler")
                amplifier.update_cycle(10, 5) #10 sec on / 5 sec off
                peltier.turn_off() #Turn Peltier cooler off
            else: 
                self.normal_mode(amplifier, peltier)  # Call normal mode
        except IOError as ioe:
            print("IOError adjusting Peltier cooler and/ or amplifiers:", ioe)
        except Exception as e:
            print("Error adjusting Peltier cooler and/ or amplifiers:", e)
        
    def normal_mode(self, amplifier, peltier):
        print("Normal mode - Amplifier is on for 5 seconds / off for 5 seconds, as long as the temperature of the amplifier is within the threshold (0°C to 40°C).")
        amplifier.update_cycle(5, 5)  #5 sec on / 5 sec off
        amplifier.turn_on_amplifiers()  #Turn amplifiers on
        peltier.turn_off()
        
        