
import math
import time


def draw_wave(amplitude, length):
    for i in range(length):
        angle = i * (math.pi / 10)
        wave_val = math.sin(angle)

        position = int(wave_val * amplitude + amplitude)

        if wave_val >= 0:
            symbol = "O"
        else:
            symbol = "*"

        print(" " * position + symbol)

        time.sleep(0.05)


length = int(input("How long should the wave be? "))

draw_wave(20, length)
