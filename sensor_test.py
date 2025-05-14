import time
from luma.core.interface.serial import spi, noop
from luma.core.render import canvas
from luma.oled.device import sh1106
import board
import busio
import adafruit_ccs811

# Initialize SPI for the OLED display using luma.oled
serial = spi(port=0, device=0, gpio=noop(), gpio_DC=23, gpio_RST=24)
device = sh1106(serial, width=128, height=64)

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
            with canvas(device) as draw:
                draw.text((0, 0), f"CO2: {eco2} ppm", fill="white")
                draw.text((0, 16), f"TVOC: {tvoc} ppb", fill="white")
        time.sleep(1)
except KeyboardInterrupt:
    print("Exiting...")
