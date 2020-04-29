# This Python file uses the following encoding: utf-8
from glob import glob

from os.path import (
    basename,
    dirname,
    isfile,
    join,
    splitext,
)

from models import (
    Core,
    Cell,
    IOCell,
    Net,
    Placement,
)

from utils import (
    floatify,
    integerify,
    numberify,
)


BENCHMARKS_DIR = join(dirname(__file__), "benchmarks")
BENCHMARK_GLOB = f'{BENCHMARKS_DIR}/*.hgr'


def get_path(path, ext='hgr'):
    return f'{splitext(path)[0]}.{ext}'


def get_benchmarks():
    return [{
        'name': splitext(basename(path))[0],
        'path': path,
        'isPlaced': isfile(get_path(path, 'csv')),
    } for path in glob(BENCHMARK_GLOB)]


def parse_hgr(hgr_file):
    with open(hgr_file) as hgr:
        num_nets, num_cells = integerify(hgr.readline().split())

        nets = []
        for i in range(num_nets):
            net = Net(i+1, integerify(hgr.readline().split()))
            nets.append(net)

        return num_cells, nets


def parse_dim(dim_file, num_cells):
    with open(dim_file) as dim:
        core = Core(numberify(dim.readline().split()))

        cells = []
        for i in range(num_cells):
            cell = Cell(i+1, floatify(dim.readline().split(",")))
            cells.append(cell)

        return core, cells


def parse_io(io_file, cells):
    with open(io_file) as io:
        num_io_cells, = integerify(io.readline().split())

        for i in range(num_io_cells):
            cells[i] = IOCell(
                cells[i],
                tuple(integerify(io.readline().split(","))),
            )

        return num_io_cells


def parse_csv(csv_file, cells):
    with open(csv_file) as csv:
        csv.readline()

        for line in csv:
            x, y, i = numberify(line.split(","))
            cells[i-1].loc = (x, y)


def load_data(path):
    if not isfile(get_path(path, 'hgr')):
        return (-1, "Missing .hgr file")

    if not isfile(get_path(path, 'dim')):
        return (-1, "Missing .dim file")

    io_present = True
    if not isfile(get_path(path, 'io')):
        io_present = False

    if not isfile(get_path(path, 'csv')):
        return (-2, "Missing .csv file")

    try:
        num_cells, nets = parse_hgr(get_path(path, 'hgr'))
    except Exception as e:
        return (
            -1,
            f"An error occured while parsing the .hgr file.\n\n{repr(e)}",
        )

    try:
        core, cells = parse_dim(get_path(path, 'dim'), num_cells)
    except Exception as e:
        return (
            -1,
            f"An error occured while parsing the .dim file.\n\n{repr(e)}",
        )

    if io_present:
        try:
            num_io_cells = parse_io(get_path(path, 'io'), cells)
        except Exception as e:
            return (
                -1,
                f"An error occured while parsing the .io file.\n\n{repr(e)}",
            )
    else:
        num_io_cells = 0

    try:
        parse_csv(get_path(path, 'csv'), cells)
    except IndexError:
        return (-1, "The .csv file references non-existing cells.")
    except Exception as e:
        return (
            -1,
            f"An error occured while parsing the .csv file.\n\n{repr(e)}",
        )

    placement = Placement(path, cells, core, nets, num_io_cells)
    return (
        0 if io_present else -3,
        placement,
    )


# if__name__ == "__main__":
#     pass
