# This Python file uses the following encoding: utf-8


class Cell:
    id = None               # Serial number (order in .dim file)
    width = None            # Cell width (μm)
    height = None           # Cell height (μm)
    power = None            # Cell power (μW)


class IOCell(Cell):
    location_pref = None    # Preferred (x, y) boundary location
    actual_location = None  # Location snapped to the nearest standard cell row


class Net:
    id = None               # Serial number (order in .hgr file)
    cells = None            # Cells that are part of the net (serial numbers)


class Core:
    width = None            # CORE width (μm)
    height = None           # CORE height (μm)
    num_rows = None         # No. of standard cell rows in CORE


class Placement:
    num_cells = None        # Number of cells
    num_io_cells = None     # Number of I/O cells
    num_nets = None         # Number of nets

    core = None             # CORE object
    c2i_h = None            # CORE-to-IO-left/right each
    c2i_v = None            # CORE-to-IO-bottom/top each


# if__name__ == "__main__":
#     pass
