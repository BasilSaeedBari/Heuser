import math
import time


def draw_wave(amplitude, length):
    """Draw an animated sine wave in the terminal."""
    for i in range(length):
        angle = i * (math.pi / 10)
        wave_val = math.sin(angle)

        # Convert the sine value into a non-negative screen position.
        position = int(amplitude * wave_val + amplitude)

        # Use a different character depending on the sine value.
        if wave_val >= 0:
            symbol = "O"
        else:
            symbol = "*"

        print(" " * position + symbol)
        time.sleep(0.05)


print("=== Animated Terminal Wave ===")
try:
    wave_length = int(input("How many lines should the wave have? "))
    if wave_length <= 0:
        print("Please enter a positive whole number.")
    else:
        draw_wave(20, wave_length)
except ValueError:
    print("Invalid input. Please enter a whole number.")
