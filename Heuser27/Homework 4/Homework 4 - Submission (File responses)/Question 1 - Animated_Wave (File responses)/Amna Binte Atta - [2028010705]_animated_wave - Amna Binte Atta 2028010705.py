# The Guided Project – Animated Terminal Wave
import math
import time
def draw_wave (amplitude,length):
    for i in range(1,length):
        angle= i * (math.pi / 10)
        wave_val = math.sin (angle)
        position = int(amplitude * wave_val + amplitude)
        if wave_val >= 0 :
            symbol = "0"
        else:
            symbol = "*"
        print(" " * position + symbol)
        time.sleep(0.05)
LENGTH = int(input("how long they want the wave to be."))
draw_wave (20,LENGTH)

