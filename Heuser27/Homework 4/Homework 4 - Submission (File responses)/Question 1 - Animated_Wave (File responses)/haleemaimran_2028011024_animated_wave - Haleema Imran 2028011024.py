import math
import time


def draw_wave(amplitude, length):
  for i in range(length):
    angle = i * (math.pi / 10)
    wave_val = math.sin(angle)
    position = int((wave_val * amplitude) + amplitude)

    if wave_val >= 0:
      symbol = "O"
    else:
      symbol = "*"

    # Print spaces and symbol
    print(" " * position + symbol)

    # STEP 7: Inside the loop, so it animates line-by-line
    time.sleep(0.05)


# STEP 8: Outside the function, at the very bottom
user_input = input("Enter how long you want the wave to be: ")
wave_length = int(user_input)

draw_wave(amplitude=20, length=wave_length)