import math
import time
def draw_wave(amplitude, length):
    for i in range(length):
        angle = i * (math.pi / 10)
        wave_val = math.sin(angle)

        position = int(wave_val * amplitude + amplitude)
        if wave_val >= 0:
            symbol = "0"
        else:
            symbol = "*"

        print(" " * position + symbol)
        time.sleep(0.05)

user_length = input("How long do you want the wave to be? ")
user_length = int(user_length)

draw_wave(20, user_length)

print("Wave complete!")