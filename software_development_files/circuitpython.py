import board
import busio
import digitalio
from adafruit_mpu6050 import MPU6050
import adafruit_sdcard
import time
import storage

# Initialize I2C bus
i2c = busio.I2C(board.SCL, board.SDA)
imu = MPU6050(i2c) # for MPU6050 sensor

# SPI pin configuration may vary, gotta adjust according to board
spi = busio.SPI(board.SCK, MISO=board.MISO, MOSI=board.MOSI) # for SD card
#  MOSI = 23 ,MISO = 22, SCK = 24

# Initialize chip select pin for SD card
cs = digitalio.DigitalInOut(board.D4)
cs.direction = digitalio.Direction.OUTPUT
cs.value = True  # Set CS high initially

# Initialize SD card
sdcard = adafruit_sdcard.SDCard(spi, cs)
vfs = storage.VfsFat(sdcard)
storage.mount(vfs, "/sd")

# Initialize LED for status indication
led = digitalio.DigitalInOut(board.D13)
led.direction = digitalio.Direction.OUTPUT
led.value = False  # Initialize LED off

# Define relay control pins
relay_pins = [
    board.D10,  # Gray - IN1
    board.D9,   # Green - IN2
    board.D6    # Blue - IN3
]

# Initialize relay control pins
relays = []
for pin in relay_pins:
    relay = digitalio.DigitalInOut(pin)
    relay.direction = digitalio.Direction.OUTPUT
    relay.value = True  # Initialize all relays on
    relays.append(relay)


# Main loop to read and save data
while True:
    try:
        gx, gy, gz = imu.gyro
        temp = imu.temperature
        data = f"GX: {gx}, GY: {gy}, GZ: {gz}, Temperature: {temp:.2f}"

        # Write data to SD card
        with open("/sd/gyroscope_data.txt", "a") as file:
            file.write(data + "\n")
            print("Data saved:", data)

        # Toggle LED
        led.value = not led.value
        time.sleep(0.1)  # Briefly toggle LED

    except Exception as e:
        print(f"Error reading or saving data: {e}")

    time.sleep(1) # Adjust delay as needed
