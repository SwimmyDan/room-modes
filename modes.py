import numpy as np

def calculate_modes(Lx,Ly,Lz, max_mode=10, max_f = -1, c=343):
    """
    TODO:
        - clean up comments and add some link for the formula
        - clean up line wraps (72)
    Calculates all eigenrequencies and room modes given room dimensions (Lx, Ly, Lz) in meters.
    Speed of Sound : c = 343 m/s @ 20 C
    
    Parameters
    ----------
    Lx : int 
        Length of room in x-direction in meters
    Ly : int 
        Length of room in y-direction in meters
    Lz : int
        Length of room in z-direction in meters
    max_mode : int
        optional maximal mode order to be iterated over
    max_f : float
        optional maximal frequency 
    c : float
        speed of sound

    Returns
    -------
    room_modes : np.ndarray
        structured (Nx5)-array of eigenfrequencies (column 0); modes (columns 1-3); and mode-type (column 4: 2 = axial, 1 = tangential, 0 = oblique). Sorted by increasing frequency. 

    Raises
    ------
    ValueError
        when the inputted parameters are not positive integers or floats
    
    """
    # ------------------- error checks ------------------- 
    if not all(isinstance(x, (int, float)) and x > 0 for x in [Lx, Ly, Lz, max_mode]):
    
        raise ValueError("Dimensions Lx, Ly, Lz and max_mode must be positive numbers.")
    
    if max_mode % 1 != 0:

        raise ValueError("Argument max_mode must be a whole number.")
    
    if max_f != -1:

        if not (isinstance(max_f, (int, float)) and max_f > 0):

            raise ValueError("Maximum frequency must be a positive number or -1")
    
    # ------------------- initialization ------------------- 
    modes_list = []
    mode_types_list = ["oblique", "tangential", "axial"]

    # ------------------- modes_array ------------------- 
    for nz in range(max_mode + 1):

        for ny in range(max_mode + 1):

            for nx in range(max_mode + 1):
                
                mode_tpl = (nx, ny, nz)

                if mode_tpl != (0,0,0):

                    f = (c/2) * np.sqrt( (nx/Lx)**2 + (ny/Ly)**2 + (nz/Lz)**2 ) # see Sarradj's script
                    f = np.round(f,2)

                    mode_type = mode_types_list[mode_tpl.count(0)] # num of zeros determine type

                    modes_list.append((f, nx, ny, nz, mode_type))

    modes_list.sort(key = lambda x : x[0])   # sorts modes by freqency

    dtype = np.dtype([                       # dtypes for structured array
        ("frequency", np.float64),
        ("nx", np.int64),
        ("ny", np.int64),
        ("nz", np.int64),
        ("mode_type", "U12")
    ])
    
    modes_array = np.array(modes_list, dtype=dtype)

    if max_f != -1:                          # cutting frequencies above max_f
        idx = np.searchsorted(
            modes_array["frequency"],
            max_f,
            side="right"
        )
        modes_array = modes_array[:idx]
    
    return modes_array