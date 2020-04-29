# This Python file uses the following encoding: utf-8
from copy import deepcopy
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


def get_benchmark_name(path):
    return splitext(basename(path))[0]


def get_placement_details(path):
    nameparts = splitext(basename(path))[0].split('_')
    benchmark = '_'.join(nameparts[0:-2])
    mode = f'Mode {nameparts[-2]}'
    algorithm = nameparts[-1].upper()
    return f"{benchmark}, {mode}, {algorithm}"


def get_benchmarks():
    return [{
        'name': get_benchmark_name(path),
        'path': path,
        'isPlaced': isfile(get_path(path, 'dim')),
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
        i = 0
        for line in csv:
            x, y, w = floatify(line.split(","))
            cells[i].loc = (x, y)
            i += 1


def load_data(path, outputPath):
    if not isfile(get_path(path, 'hgr')):
        return (-1, "Missing .hgr file")

    if not isfile(get_path(path, 'dim')):
        return (-1, "Missing .dim file")

    benchmark_name = get_benchmark_name(path)
    csv_files = glob(f'{outputPath}/{benchmark_name}_?_?fs.csv')

    if len(csv_files) == 0:
        return (-1, "No generated placement files (.csv) found")

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

    placements = []

    for csv_file in csv_files:
        placed_cells = deepcopy(cells)
        try:
            parse_csv(csv_file, placed_cells)
        except IndexError:
            return (
                -1,
                f"{basename(csv_file)} references non-existing cells."
            )
        except Exception as e:
            return (
                -1,
                f"An error occured while parsing {basename(csv_file)}.\n"
                f"\n{repr(e)}",
            )
        placement = Placement(path, csv_file, placed_cells, core, nets)
        placements.append(placement)

    return (0, placements)


# if__name__ == "__main__":
#     pass
