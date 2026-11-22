import math
import time


def draw_wave(amplitude, length):
    for i in range(length):

        # Calculate the angle
        angle = i * (math.pi / 10)

        # Calculate sine
        wave_val = math.sin(angle)

        # Calculate the position
        position = int(amplitude * (wave_val + 1))

        # Conditional statement
        if wave_val >= 0:
            symbol = "O"
        else:
            symbol = "*"

        # Print the wave
        print(" " * position + symbol)

        # Create animation
        time.sleep(0.05)


# Ask the user for the length
length = int(input("How long do you want the wave to be? "))

# Call the function
draw_wave(20, length)