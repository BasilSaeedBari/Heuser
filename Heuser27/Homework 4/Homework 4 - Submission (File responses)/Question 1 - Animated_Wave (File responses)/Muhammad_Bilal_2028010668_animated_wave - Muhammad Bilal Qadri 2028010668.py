#Importing Libraries
import math
import time

#Defining a function in which it calculates wave angle, its position and symbol
def draw_wave(amplitude,length):
    for i in range(length+1):
        formula = i * (math.pi / 10)
        wave_val= math.sin(formula)
        
        position = int((wave_val * amplitude) + amplitude)
        
        if wave_val >=0:
            print(" " * position + "O")
        else:
            print(" " * position + "*")
        time.sleep(0.05) #Animation effect 

#Asking user for input for length of wave
userIN= int(input("Enter the length for the wave:"))


draw_wave(20,userIN)            
        