import numpy as np
import pandas as pd


def calculate_room_modes(Lx,Ly,Lz, max_mode=5):
    """

    Calculates all eigenrequencies and room modes given room dimensions (Lx, Ly, Lz) (m).
    Speed of Sound : c = 343 m/s @ 20 C
    
    Parameters
    ----------
    Lx : int 
        Length of room in x-direction
    Ly : int 
        Length of room in y-direction
    Lz : int
        Length of room in z-direction
    max_mode : int
        maximal mode order to be iterated over

    Returns
    -------
    room_modes : pd.Dataframe
        Pandas dataframe of eigenfrequencies, modes and types of modes sorted by increasing frequency 

    Raises
    ------
    ValueError
        when the inputted parameters are not positive integers or floats
    
    """
    c = 343 # sound speed
    modes_list = [] # to be used to initialize dataframe later

    if not all(isinstance(x, (int, float)) and x > 0 for x in [Lx, Ly, Lz, max_mode]):
    
        raise ValueError("Dimensions Lx, Ly, Lz and max_mode must be positive numbers.")
    
    for nz in range(max_mode + 1):

        for ny in range(max_mode + 1):

            for nx in range(max_mode + 1):
                
                mode_tpl = (nx, ny, nz)

                if mode_tpl != (0,0,0):

                    f = (c/2) * np.sqrt( (nx/Lx)**2 + (ny/Ly)**2 + (nz/Lz)**2 ) # see Sarradj's script
                    f = np.round(f,2)

                    mode_types_list = ["oblique", "tangential", "axial"]
                    mode_type = mode_types_list[mode_tpl.count(0)] # num of zeros determine type

                    modes_list.append([f, (nx,ny,nz), mode_type])

    modes_df = pd.DataFrame(data = modes_list, columns = ["frequency", "mode", "type"]) # initialize dataframe
    modes_df.sort_values(by = "frequency", inplace= True)
    
    return modes_df