def calculate_room_modes(Lx,Ly,Lz,max_mode=5):
    """
    Calculates all eigenrequencies and room modes given room dimensions (Lx, Ly, Lz).

    Parameters
    ----------
    first : array_like
        the 1st param name `first`
    second :
        the 2nd param
    third : {'value', 'other'}, optional
        the 3rd param, by default 'value'

    Returns
    -------
    string
        a value in a string

    Raises
    ------
    KeyError
        when a key error
    OtherError
        when an other error
    
    """
    
    return Lx*Ly*Lz