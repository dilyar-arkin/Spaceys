import machine
import time
import sdcard
import uos
import utime

# this sd card object class will initialize and read/store values to both microSD card and SD card. 
class sdcard_init:
    name = 'sd_card_reader'
    def __init__(self, cs_in,mosi_in,miso_in,sck_in,gate):
        #self.name = name    # instance variable unique to each instance
        # Assign chip select (CS) pin (and start it high)
        # If pin configuration on pico changes, update pin number here
        self.cs = machine.Pin(cs_in, machine.Pin.OUT)

        # Intialize SPI peripheral (start with 1 MHz)
        # Current pinout config mapping GPIO to sdcard reader board :
        # for microSd card : GP10: CLK ; GP11: DI ; GP12: DO ; GP13: CS, Gate : 1;
        # for sd card CS: 5, MOSI: GP7, MISO: GP4, SCK: GP6, Gate: 0)
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
        uos.mount(self.vfs, "/sd")
        
    def write (self, filename, val):
        #print(self.name)
        # Create a file if not created already and write sensor values to it
        filepath = f"/sd/{filename}.txt" #to avoid creation of unnecessary files
        current_time = utime.time()
        time_tuple = utime.localtime(current_time)
        timestamp = "{:04d}-{:02d}-{:02d} {:02d}:{:02d}:{:02d}".format(
            time_tuple[0], time_tuple[1], time_tuple[2],  # Year, Month, Day
            time_tuple[3], time_tuple[4], time_tuple[5]   # Hour, Minute, Second
        )
        with open(filepath, "a") as file:
            file.write(f"{timestamp}\t{val}\r\n")
            print(f"Data stored in {filename}.txt")           

    def read (self, filename):
        filepath = f"/sd/{filename}.txt"
        # Open the file and read from it
        try:
            with open(filepath, "r") as file:
                data = file.read()
                #print(data)
                return data
        except OSError as e:
            print(f"Error reading file: {e}")
    