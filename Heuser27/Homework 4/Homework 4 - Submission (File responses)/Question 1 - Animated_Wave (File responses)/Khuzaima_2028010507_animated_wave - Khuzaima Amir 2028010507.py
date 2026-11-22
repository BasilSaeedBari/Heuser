import math
import time


def draw_wave(user_length):
    for i in range(user_length):
        angle = i * (math.pi / 10)
        wave_val = math.sin(angle)

        position = int(wave_val * 20 + 20)

        if wave_val >= 0:
            symbol = "O"
        else:
            symbol = "*"

        print(" " * position + symbol)
        time.sleep(0.05)


user_length = int(
    input("How long should the wave be?  "))
draw_wave(user_length)
