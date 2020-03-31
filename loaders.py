# This Python file uses the following encoding: utf-8
from glob import glob
from os.path import basename, join, splitext

from models import Net
from utils import integerify


BENCHMARKS_DIR = 'benchmarks'
BENCHMARK_GLOB = f'{BENCHMARKS_DIR}/*.hgr'


def get_benchmarks():
    return [splitext(basename(path))[0] for path in glob(BENCHMARK_GLOB)]


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


def load_data(benchmark):
    hgr_file = join(BENCHMARKS_DIR, f'{benchmark}.hgr')
    dim_file = join(BENCHMARKS_DIR, f'{benchmark}.dim')
    io_file = join(BENCHMARKS_DIR, f'{benchmark}.io')
    csv_file = join(BENCHMARKS_DIR, f'{benchmark}.csv')


# if__name__ == "__main__":
#     pass
