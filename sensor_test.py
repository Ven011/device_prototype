import time
import pygame
import board
import busio
import adafruit_ccs811

# Initialize pygame
pygame.init()
window_size = (320, 120)
screen = pygame.display.set_mode(window_size)
pygame.display.set_caption("Sensor Data Display")
font = pygame.font.SysFont(None, 36)

# I2C setup
i2c = busio.I2C(board.SCL, board.SDA)

# Sensor init
ccs811 = adafruit_ccs811.CCS811(i2c, address=0x5A)

# Display sensor data
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
            timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
            print(f"[{timestamp}] CO2: {eco2} ppm, TVOC: {tvoc} ppb")
            co2_text = font.render(f"CO2: {eco2} ppm", True, (255, 255, 255))
            tvoc_text = font.render(f"TVOC: {tvoc} ppb", True, (255, 255, 255))
            time_text = font.render(timestamp, True, (180, 180, 180))
            screen.blit(co2_text, (10, 20))
            screen.blit(tvoc_text, (10, 60))
            screen.blit(time_text, (10, 90))
        pygame.display.flip()
        time.sleep(1)
except KeyboardInterrupt:
    print("Exiting...")
finally:
    pygame.quit()
