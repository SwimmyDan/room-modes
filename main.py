from modes import calculate_modes
from visualization import make_resonance_plot, make_pressure_plot
from export import save_modes_csv, save_modes_txt

if __name__ == "__main__":
    
    # Room dimensions in meters
    Lx = 8.2
    Ly = 5.2
    Lz = 3.1

    # Calculation settings
    max_mode = 10
    max_f = 200
    c = 343 #speed of sound in m/s

    # Visualization settings
    modes_plotted = 3
    step_size = 0.5
    pressure_factor = 2

    print(f"Room dimensions: Lx = {Lx}, Ly = {Ly}, Lz = {Lz}")
    
    # Calculate room modes
    room_modes = calculate_modes(
        Lx,Ly,Lz, 
        max_mode=max_mode, 
        max_f = max_f,
        c = c
    )

    # Export results
    save_modes_csv(room_modes)
    save_modes_txt(room_modes, filename= 'modes.txt') 
    #change to 'modes.md' for markdown

    print(
        "Tables generated at "
        "\"outputs\\modes.txt\" "
        "and "
        "\"outputs\\modes.csv\""
    )

    # Generate visualizations
    make_resonance_plot(
        room_modes, 
        max_f,
        Lx,Ly,Lz
    )
    print(
        "Resonance plot generated at "
        f"\"outputs\\{Lx}x{Ly}x{Lz}_resonance_plot.png\""
    )

    make_pressure_plot(
        Lx, Ly, Lz, 
        room_modes, 
        modes_plotted, 
        step_size, 
        pressure_factor
    )
