import machine
import time
import sdcard
import uos

class sdcard_init:
    name = 'Unknown IO'
    def __init__(self, name,cs_in,mosi_in,miso_in,sck_in,gate):
        self.name = name    # instance variable unique to each instance
        # Assign chip select (CS) pin (and start it high)
        # If pin configuration on pico changes, update pin number here
        self.cs = machine.Pin(cs_in, machine.Pin.OUT)

        # Intialize SPI peripheral (start with 1 MHz)
        # Current pinout config mapping GPIO to sdcard reader board :
        # GP10: CLK ; GP11: DI ; GP12: DO ; GP13: CS; PIN13 : GND
        self.spi = machine.SPI(gate,
                baudrate=1000000,
                polarity=0,
                phase=0,
                bits=8,
                firstbit=machine.SPI.MSB,
                sck=machine.Pin(sck_in),
                mosi=machine.Pin(mosi_in),
                miso=machine.Pin(miso_in))

        # Initialize SD card
        self.sd = sdcard.SDCard(self.spi, self.cs)
        # Mount filesystem
        self.vfs = uos.VfsFat(self.sd)
        self.uos.mount(self.vfs, "/sd")
            

    def write (self, val):
        #print(self.name)
        # Create a file if not created already and write sensor values to it
        with open(f"/sd/{self.name}.txt", "a") as file:
            #print(machine.RTC().datetime())
            file.write(f"{time.time_ns()}\t")
            file.write(f"{val}\r\n")
    
    def read (self):
        # Open the file and read from it
        with open(f"/sd/{self.name}.txt", "r") as file:
            data = file.read()
            #print(data)
            return data
