import math
import time


def draw_wave(amplitude, length):
    """Print an animated sine wave in the terminal."""
    for i in range(length):
        angle = i * (math.pi / 10)
        wave_val = math.sin(angle)

        # sin() is between -1 and 1, so shift by amplitude to keep it non-negative
        position = int(wave_val * amplitude + amplitude)

        if wave_val >= 0:
            symbol = "O"
        else:
            symbol = "*"

        print(" " * position + symbol)
        time.sleep(0.05)


length = int(input("How long do you want the wave to be? "))
draw_wave(20, length)
