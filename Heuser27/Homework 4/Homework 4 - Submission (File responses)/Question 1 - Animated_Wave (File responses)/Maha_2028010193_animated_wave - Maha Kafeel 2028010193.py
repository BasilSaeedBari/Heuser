import math
import time

def draw_wave(amplitude, length):
    for i in range(length):
        angle = i * (math.pi / 10)
        wave_val = (math.sin(angle) * amplitude) + amplitude
        position = int(wave_val)
        if wave_val >= 0:
            symbol = "0"
        else:
            symbol = "*"
        print(" " * position + symbol)
        time.sleep(0.05)

user_input = input("How long do you want the wave to be? ")
length_val = int(user_input)
draw_wave(20, length_val)