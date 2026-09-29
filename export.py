import numpy as np
from pathlib import Path
def save_modes_csv(room_modes, filename = 'modes.csv'):

    np.savetxt(
        Path( "outputs") / filename,
        room_modes,
        delimiter=",",
        fmt = ["%.2f", "%d", "%d", "%d", "%s"],
        header="frequency,nx,ny,nz,mode_type"
    )

def save_modes_txt(room_modes, filename = 'modes.txt', title = 'Mode Table'):

    with open(Path ("outputs") / filename, "w") as f:

        # Title
        f.write(f"{title}\n\n")

        # Markdown header
        f.write("| frequency | nx | ny | nz | mode_type |\n")
        f.write("|----------:|---:|---:|---:|-----------|\n")

        # Data rows
        for row in room_modes:
            f.write(
                f"| {row['frequency']:.2f} "
                f"| {row['nx']} "
                f"| {row['ny']} "
                f"| {row['nz']} "
                f"| {row['mode_type']} |\n"
            )