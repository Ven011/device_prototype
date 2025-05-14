import time
import board
import busio
import adafruit_ccs811
import RPi.GPIO as GPIO
import spidev
import sh1106


# Initialize SPI for the OLED display
GPIO.setmode(GPIO.BCM)
DC_PIN = 5
CS_PIN = 26
RES_PIN = 6
GPIO.setup(DC_PIN, GPIO.OUT)
GPIO.setup(CS_PIN, GPIO.OUT)
GPIO.setup(RES_PIN, GPIO.OUT)
spi = spidev.SpiDev()
spi.open(1, 0) # SPI bus 1, device 0
spi.max_speed_hz = 8000000  # 8 MHz
oled = sh1106.SH1106_SPI(128, 64, spi, DC_PIN, RES_PIN, CS_PIN)

oled.init_display()
oled.text("Hello World!", 0, 0, 1)
oled.show()

# I2C setup
i2c = busio.I2C(board.SCL, board.SDA)

# Sensor init
ccs811 = adafruit_ccs811.CCS811(i2c)

# Display sensor data
try:
    while True:
        if ccs811.data_ready:
            eco2 = ccs811.eco2
            tvoc = ccs811.tvoc
            print(f"CO2: {eco2} ppm, TVOC: {tvoc} ppb")
        time.sleep(1)
except KeyboardInterrupt:
    print("Exiting...")
