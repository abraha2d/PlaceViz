# This Python file uses the following encoding: utf-8


class Cell:
    id = None               # Serial number (order in .dim file)
    width = None            # Cell width (μm)
    height = None           # Cell height (μm)
    power = None            # Cell power (μW)
    loc = None              # (x, y) (snapped to the nearest standard cell row)

    def __init__(self, id, cell_data):
        self.id = id
        self.width, self.height, self.power = cell_data


class IOCell(Cell):
    loc_pref = None         # Preferred (x, y) boundary location

    def __init__(self, cell, loc_pref):
        self.id = cell.id
        self.width, self.height = cell.width, cell.height
        self.power = cell.power
        self.loc_pref = loc_pref


class Net:
    id = None               # Serial number (order in .hgr file)
    cells = None            # Cells that are part of the net (serial numbers)

    def __init__(self, id, cells):
        self.id = id
        self.cells = cells


class Core:
    width = None            # CORE width (μm)
    height = None           # CORE height (μm)
    c2i_h = None            # CORE-to-IO-left/right each
    c2i_v = None            # CORE-to-IO-bottom/top each
    num_rows = None         # No. of standard cell rows in CORE

    def __init__(self, core_data):
        self.width, self.height, self.c2i_h, self.c2i_v, self.num_rows = core_data


class Placement:
    num_io_cells = None     # Number of I/O cells

    cells = None            # List of cells
    core = None             # CORE object
    nets = None             # List of nets

    def __init__(self, path, cells, core, nets, num_io_cells):
        self.path = path
        self.cells = cells
        self.core = core
        self.nets = nets
        self.num_io_cells = num_io_cells


# if__name__ == "__main__":
#     pass
