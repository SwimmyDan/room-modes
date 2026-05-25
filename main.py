import numpy as np
import matplotlib.pyplot as plt
from modes import calculate_room_modes

print("Modules imported.")

if __name__ == "__main__":
    
    Lx = 3
    Ly = 3
    Lz = 3
    print(f"Room dimensions: Lx = {Lx}, Ly = {Ly}, Lz = {Lz}")
    
    print("Room modes are")
    print(calculate_room_modes(Lx,Ly,Lz))