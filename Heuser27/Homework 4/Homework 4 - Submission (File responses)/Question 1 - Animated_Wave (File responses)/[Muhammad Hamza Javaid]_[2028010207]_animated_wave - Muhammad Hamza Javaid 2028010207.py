import time, math

def draw_wave(amplitude, length):
    
    for i in range(length):
        
        angle = i * (math.pi / 10)
        wave_val = math.sin(angle)
        pos = int(wave_val * amplitude + amplitude)
        
        if wave_val >= 0:
            symbol = "0"
        else:
            symbol = "*"
        
        print(" " * pos + symbol)
        
        time.sleep(0.05)
    
length = int(input("How long do you want the wave to be (in terms of lines): "))
draw_wave(20, length)