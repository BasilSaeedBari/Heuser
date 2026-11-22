import math
import time

def draw_wave(amplitude, length):
    for i in range(length):
        angle = i * (math.pi / 10)
        wave_val = math.sin(angle)

        position = int(amplitude * wave_val + amplitude)

        if wave_val >= 0:
            symbol = "O"
        else:
            symbol = "*"

        print(" " * position + symbol)
        time.sleep(0.05)

wave_length = int(input("How many lines should the wave have? "))
draw_wave(20, wave_length)