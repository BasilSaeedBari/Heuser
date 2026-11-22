import math
import time

def draw_wave(amplitude, length):
    for i in range(length):
        angle = i * (math.pi / 10)
        wave_val = math.sin(angle)
        space = int(wave_val * amplitude + amplitude)

        if wave_val >= 0:
            symbol = 'O'
        else:
            symbol = '*'

        print(" " * space + symbol)
        time.sleep(0.05)

length = int(input("Enter the length for your wave: "))
draw_wave(20, length)