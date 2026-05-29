import numpy as np
import pandas as pd
from pathlib import Path
import matplotlib.pyplot as plt
from modes import calculate_room_modes

print("Modules imported.")

if __name__ == "__main__":
    
    Lx = 0.5
    Ly = 1
    Lz = 2
    
    print(f"Room dimensions: Lx = {Lx}, Ly = {Ly}, Lz = {Lz}")
    
    room_modes = calculate_room_modes(Lx,Ly,Lz, max_mode = 3)

    print("Room modes are")
    print(room_modes)
    print("Output saved.")
    
    room_modes.to_csv( Path('outputs') / "modes.csv", index = False)
    
    with open( Path('outputs') / "modes.txt", "w" ) as f:
        
        f.write(room_modes.to_string(index=False))
        