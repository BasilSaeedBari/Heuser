# animated_wave.py
# Part 1: The Guided Project - Animated Terminal Wave
#
# This program "draws" an animated, oscillating sine wave directly in the
# terminal. It demonstrates built-in functions, imported libraries, library
# functions and constants, a custom function, a loop, and a conditional.

# Step 1: Setup & Imports
import math   # gives us math.sin() and math.pi
import time   # gives us time.sleep() for the animation


# Step 2: Define Your Function
# draw_wave takes two arguments:
#   amplitude -> how wide the wave gets
#   length    -> how many lines to print
def draw_wave(amplitude, length):

    # Step 3: The Iteration Loop
    # Loop over a range() generated from the length argument.
    for i in range(length):

        # Step 4: The Math (Inside the Loop)
        # Calculate the current angle using math.pi (a library constant).
        angle = i * (math.pi / 10)
        # Calculate the sine of that angle using math.sin() (a library function).
        wave_val = math.sin(angle)

        # Step 5: The Logic (Inside the Loop)
        # math.sin() returns a value between -1.0 and 1.0.
        # Multiply by amplitude, then add amplitude so it is never negative.
        # Use the built-in int() to round it to a whole number of spaces.
        position = int(wave_val * amplitude + amplitude)

        # Step 6: Conditionals & Output (Inside the Loop)
        # Pick a symbol based on the wave's value.
        if wave_val >= 0:
            symbol = "0"
        else:
            symbol = "*"

        # Print spaces to push the symbol across the screen, then the symbol.
        print(" " * position + symbol)

        # Step 7: Animation
        # Pause for a fraction of a second so the wave appears to scroll.
        time.sleep(0.05)


# Step 8: User Input
# Ask the user how long they want the wave, convert it to an integer with int(),
# then call draw_wave() with an amplitude of 20 and the user's chosen length.
user_answer = input("How many lines long should the wave be? ")
length = int(user_answer)
draw_wave(20, length)