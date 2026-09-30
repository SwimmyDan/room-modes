import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path

def make_resonance_plot(room_modes, max_f, Lx,Ly,Lz):
    """
    Create and save a resonance map of the room modes.

    Generates a stem plot of the room's resonance frequencies, with
    axial, tangential, and oblique modes distinguished by color and
    vertical position. The frequency axis uses a logarithmic scale,
    with a secondary axis showing nominal 1/3-octave band centers.

    The plot is saved as a PNG file in the 'outputs' folder.

    Parameters
    ----------
    room_modes : numpy.ndarray
        Structured NumPy array containing the room modes. Must include
        the fields 'frequency', 'nx', 'ny', 'nz' and 'mode_type'. The 
        'mode_type' field should contain 'axial', 'tangential', or 
        'oblique'.
    max_f : float
        Maximum frequency in Hz to display in the plot. If -1, the
        maximum frequency is determined from room_modes.
    Lx : float
        Length of the room in the x-direction, in meters. Used in the
        output filename.
    Ly : float
        Length of the room in the y-direction, in meters. Used in the
        output filename.
    Lz : float
        Height of the room in meters. Used in the output filename.

    Returns
    -------
    None
        The plot is saved as a PNG file. No value is returned.

    Raises
    ------
    KeyError
        If the required columns are missing from room_modes.
    """

    # seperate array into mode types 
    modes_ax = room_modes[room_modes['mode_type'] == 'axial']['frequency']
    modes_tan = room_modes[room_modes['mode_type'] == 'tangential']['frequency']
    modes_obl = room_modes[room_modes['mode_type'] == 'oblique']['frequency']

    # -------------------- Stem Data --------------------
    fig, ax = plt.subplots(figsize=(12,3), layout = 'constrained')
    if len(modes_ax) != 0:
        ax.stem(modes_ax, np.ones(len(modes_ax)), linefmt = 'red', markerfmt = '', label = 'axial', basefmt =' ')
    if len(modes_tan) != 0:
        ax.stem(modes_tan, 0.66*np.ones(len(modes_tan)), linefmt = 'blue', markerfmt = '', label = 'tangential', basefmt =' ')
    if len(modes_obl) != 0:
        ax.stem(modes_obl, 0.33*np.ones(len(modes_obl)), linefmt = 'black', markerfmt = '', label = 'oblique', basefmt =' ')


    # -------------------- Title, Legend --------------------
    if max_f == -1:
        max_f = room_modes['frequency'][-1]
    ax.set_title(f'Room modes up to {max_f} Hz')
    ax.legend(loc='upper center', bbox_to_anchor=(0.5, -0.1), ncol=3, frameon = False)


    # -------------------- Bottom Axis --------------------

    # limits, scale
    max_tick = np.ceil(room_modes['frequency'][-1] / 20) * 20 + 10
    ax.set_xscale('log')
    ax.set_xlim(20, max_tick)
    ax.set_ylim(0, 1.1)

    # labelled major ticks
    major_ticks = np.concatenate((
        np.arange(20, min(max_tick, 100) + 1, 10),
        np.arange(100, min(max_tick, 1000) + 1, 100),
        np.arange(1000, max_tick + 1, 1000)
    ))
    ax.set_xticks(major_ticks)
    ax.set_xticklabels([f'{f:g}' for f in major_ticks])

    # unlabelled 5 Hz minor ticks
    all_ticks = np.arange(20, max_tick + 5, 5)
    minor_ticks = all_ticks[~np.isin(all_ticks, major_ticks)]
    ax.set_xticks(minor_ticks, minor=True)
    ax.set_xticklabels([''] * len(minor_ticks), minor=True)
    ax.tick_params(axis='x', which='minor', length=4)


    # -------------------- Top Axis --------------------

    ax_top = ax.twiny()
    ax_top.set_xscale('log')
    ax_top.set_xlim(20, max_tick)
    ax_top.set_yticks([])

    # nominal 1/3-octave band centers
    centers = np.array([
    25, 31.5, 40, 50, 63, 80, 100, 125, 160, 200, 250,
    315, 400, 500, 630, 800, 1000, 1250, 1600, 2000,
    2500, 3150, 4000, 5000, 6300, 8000, 10000, 12500,
    16000, 20000
    ])

    # only keep centers within axis limits
    centers = centers[(centers >= 20) & (centers <= max_tick)]

    # band boundaries
    minor = np.concatenate((
        [centers[0] / 2**(1/6)],
        centers[:-1] * 2**(1/6)
    ))

    # labelled major ticks
    ax_top.set_xticks(centers)
    ax_top.set_xticklabels([f'{f:g}' for f in centers])

    # unlabelled minor ticks / band edges
    ax_top.set_xticks(minor, minor=True)
    ax_top.tick_params(
        axis='x',
        which='minor',
        length=4,
        labeltop = False
    )

    # band edge grid lines
    for f in minor:
        ax.axvline(f, linestyle='--', linewidth=0.8, alpha=0.5)

    # final output
    fig.savefig(Path('outputs') / f'{Lx}x{Ly}x{Lz}_resonance_plot.png')

def make_pressure_plot(Lx, Ly, Lz, room_modes, modes_plotted, step_size = 0.5, pressure_factor = 2):
    """
    Generate and save 3D pressure distribution plots for room modes.

    For each selected room mode, calculates the normalized pressure
    distribution throughout the room using the modal indices nx, ny,
    and nz. The pressure distribution is visualized using colored
    voxels, with red representing positive pressure and blue
    representing negative pressure. Voxel opacity is determined by
    the absolute pressure raised to the specified pressure_factor.

    Each mode is visualized from four different viewing angles in a
    2x2 subplot layout. The plots are saved as PNG files in the
    'outputs' directory.

    Parameters
    ----------
    Lx : float
        Length of the room in the x-direction, in meters.
    Ly : float
        Length of the room in the y-direction, in meters.
    Lz : float
        Height of the room in meters.
    room_modes : numpy.ndarray
        Structured NumPy array containing the room modes. Must include
        the fields 'frequency', 'nx', 'ny', and 'nz'. Each row
        represents a mode.
    modes_plotted : int
        Number of room modes to plot, starting from the first row of
        room_modes. If 0, no plots are generated. The number of plots
        is limited by the number of available rows.
    step_size : float, optional
        Voxel size in meters, used to discretize the room for the
        pressure calculation. Smaller values produce finer spatial
        resolution but increase computational cost. Default is 0.5.
    pressure_factor : float, optional
        Exponent applied to the absolute pressure values to control
        voxel opacity. Larger values emphasize regions of high
        pressure. Default is 2.

    Returns
    -------
    None
        The plots are saved as PNG files. No value is returned.

    Raises
    ------
    ValueError
        If any room dimension, step_size, or pressure_factor is not
        a positive number, or if modes_plotted is not a non-negative
        integer.
    """

    # ------------------- Error Checks ------------------- 
    dimensions = [Lx, Ly, Lz, step_size, pressure_factor]
    if not all(
        isinstance(x, (int, float)) and x > 0
        for x in dimensions
    ):
        raise ValueError(
            "Dimensions Lx, Ly, Lz, pressure_factor and step_size"
            "must be real positive numbers."
        )
    
    if not ( 
        isinstance(modes_plotted, int) 
        and modes_plotted >= 0 
    ):
         raise ValueError(
             "modes_plotted must be a positive whole number."
             )

    if 4 * step_size > min(Lx,Ly,Lz):
        print(
            f"*** Caution! A large step_size ({step_size} m) "
            "results in inaccurate plots! ***"
        )
    
    # ------------------- Early Return -------------------
    if modes_plotted == 0:
            print('No pressure plots generated.')
            return
    
    # ------------------- Helper Function -------------------
    def make_voxels(ax):
        """Plots voxel cubes and set aspect ratio."""
        ax.voxels(
            *coords,
            filled,
            facecolors=facecolors,
            edgecolors='none',
            shade=False
        )
        ax.set_box_aspect((Lx, Ly, Lz))

    # ------------------- Main Logic -------------------
    modes_plotted = min(room_modes.shape[0], modes_plotted)
    for i in range(modes_plotted):

        f = room_modes['frequency'][i]
        nx = room_modes['nx'][i]
        ny = room_modes['ny'][i]
        nz = room_modes['nz'][i]
        dx = step_size

        # edges for voxel locations in ax.voxels
        x_edges = np.append(np.arange(0, Lx, dx), Lx)
        y_edges = np.append(np.arange(0, Ly, dx), Ly)
        z_edges = np.append(np.arange(0, Lz, dx), Lz)
        
        coords = np.meshgrid(
            x_edges,
            y_edges,
            z_edges,
            indexing = 'ij'
        )

        # centers for calculating pressure scalars
        x = (x_edges[:-1] + x_edges[1:]) / 2
        y = (y_edges[:-1] + y_edges[1:]) / 2
        z = (z_edges[:-1] + z_edges[1:]) / 2        


        X, Y, Z = np.meshgrid(x,y,z, indexing='ij')

        P = (
            np.cos(nx*np.pi*X/Lx) 
            * np.cos(ny*np.pi*Y/Ly) 
            * np.cos(nz*np.pi*Z/Lz)
        )
        A = np.abs(P)

        R = np.where(P > 0, 1, 0) # red for postive pressure
        G = np.zeros_like(P)
        B = np.where(P < 0, 1, 0) # blue for negative pressure

        A = A ** pressure_factor # exagerates alphas

        facecolors = np.stack([R,G,B,A], axis=-1)

        #filled = A.astype(bool) # for filling all voxels
        filled = A > 0.05 # for skipping near-0 areas 

        fig = plt.figure(figsize=(10, 7), layout='constrained')
    
        ax1 = fig.add_subplot(221, projection='3d')
        ax2 = fig.add_subplot(222, projection='3d')
        ax3 = fig.add_subplot(223, projection='3d')
        ax4 = fig.add_subplot(224, projection='3d')

        for ax in (ax1,ax2,ax3,ax4):
            make_voxels(ax)

        ax1.view_init(elev=30, azim=-35)
        ax2.view_init(elev=0,azim=90)
        ax3.view_init(elev=90, azim=0)
        ax4.view_init(elev=0, azim=180)

        ax2.set_yticks([])
        ax3.set_zticks([])
        ax4.set_xticks([])

        title_str = (
            f"({nx},{ny},{nz})-mode at {f} Hz."
            "Red = positive, Blue = negative."
        )

        fig.text(
            0.5, 0.02,
            title_str,
            ha="center",
            va="bottom",
            fontsize = 16
        )

        plt.savefig(
            Path('outputs') 
            / f'{Lx}x{Ly}x{Lz}_pressure_plot_{f}_Hz_{i}.png',
            bbox_inches="tight"
        )

        print(
            "Pressure plot generated at "
            f"\"outputs\\{Lx}x{Ly}x{Lz}_pressure_plot_{f}_Hz_{i}.png\"."
        )