# This Python file uses the following encoding: utf-8
from glob import glob
from os.path import (
    basename,
    isfile,
    join,
    splitext,
)

from models import Net
from utils import integerify


BENCHMARKS_DIR = 'benchmarks'
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
            net = Net()
            net.id = i
            net.cells = integerify(hgr.readline().split())
            nets.append(net)
        assert len(nets) == num_nets
        return nets


def load_data(path):
    if not isfile(get_path(path, 'hgr')):
        return (-1, "Missing .hgr file")

    if not isfile(get_path(path, 'dim')):
        return (-1, "Missing .dim file")

    if not isfile(get_path(path, 'io')):
        return (-1, "Missing .io file")

    if not isfile(get_path(path, 'csv')):
        return (-2, "Missing .csv file")

    return (-1, "Success.")


def load_benchmark(benchmark):
    return load_data(join(BENCHMARKS_DIR, f'{benchmark}.hgr'))

    # if__name__ == "__main__":
#     pass
