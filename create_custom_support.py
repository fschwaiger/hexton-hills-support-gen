
import sys, os, glob
import numpy as np
from stl import mesh
import math
from tqdm import tqdm


def load_mesh(file):
    return mesh.Mesh.from_file(file)


def realign_mesh(tile):
    min = tile.min_
    max = tile.max_
    mean = (min + max) / 2
    tile.points[:,(0,3,6)] -= mean[0]
    tile.points[:,(1,4,7)] -= mean[1]
    tile.points[:,(2,5,8)] -= min[2]
    return tile


def rotate_mesh(tile):
    tile.rotate([-0.5, 0, 0], math.radians(27.5))
    return tile


def add_support(tile):
    # support = mesh.Mesh.from_file('support_1.0.stl')
    # support.points[:,(0,3,6)] += -60.7
    # support.points[:,(1,4,7)] += -37.6
    # support.points[:,(2,5,8)] += -17.5
    support = mesh.Mesh.from_file('support_1.0_noside.stl')
    support.points[:,(0,3,6)] += -60.7
    support.points[:,(1,4,7)] += -36.7
    support.points[:,(2,5,8)] += -17.5
    tile = mesh.Mesh(np.concatenate([tile.data,support.data]))
    return tile


def write_output(tile, file):
    tile.save(file.replace('less.stl', 's.stl'))


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print('''
    Usage: python create_custom_support.py path/to/tiles/with_*_wildcard.stl''')
    else:
        for file in tqdm([g for f in sys.argv[1:] for g in glob.glob(f)]):
            tile = load_mesh(file)
            tile = realign_mesh(tile)
            tile = rotate_mesh(tile)
            tile = add_support(tile)
            write_output(tile, file)

