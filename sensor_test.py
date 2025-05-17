import time
import pygame
import board
import busio
import adafruit_ccs811
from luma.core.interface.serial import i2c
from luma.oled.device import sh1106
from luma.core.render import canvas

# Initialize pygame
pygame.init()
window_size = (320, 120)
screen = pygame.display.set_mode(window_size)
pygame.display.set_caption("Sensor Data Display")
font = pygame.font.SysFont(None, 36)

# I2C setup for sensor
sensor_i2c = busio.I2C(board.SCL, board.SDA)

# Sensor init (address 0x5A)
ccs811 = adafruit_ccs811.CCS811(sensor_i2c, address=0x5A)

# I2C setup for OLED (address 0x3C)
display_serial = i2c(port=1, address=0x3C)
oled = sh1106(display_serial, width=128, height=64)

try:
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        screen.fill((0, 0, 0))
        if ccs811.data_ready:
            eco2 = ccs811.eco2
            tvoc = ccs811.tvoc
            print(f"CO2: {eco2} ppm, TVOC: {tvoc} ppb")
            co2_text = font.render(f"CO2: {eco2} ppm", True, (255, 255, 255))
            tvoc_text = font.render(f"TVOC: {tvoc} ppb", True, (255, 255, 255))
            screen.blit(co2_text, (10, 20))
            screen.blit(tvoc_text, (10, 60))
            with canvas(oled) as draw:
                draw.text((0, 10), f"CO2: {eco2} ppm", fill="yellow")
                draw.text((0, 30), f"TVOC: {tvoc} ppb", fill="yellow")
        pygame.display.flip()
        time.sleep(1)
except KeyboardInterrupt:
    print("Exiting...")
finally:
    pygame.quit()
