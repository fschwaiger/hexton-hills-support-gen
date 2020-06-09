
import sys, os, glob
import numpy as np
from stl import mesh
import math


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
    support = mesh.Mesh.from_file('support.stl')
    support.points[:,(0,3,6)] += -60.7
    support.points[:,(1,4,7)] += -36.6
    support.points[:,(2,5,8)] += -18.5
    tile = mesh.Mesh(np.concatenate([tile.data,support.data]))
    return tile


def write_output(tile, file):
    tile.save(file.replace('.stl', '_supported.stl'))
    print(file)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        files = glob.glob('../supportless/*supportless.stl')
    else:
        files = sys.argv[1:]

    for file in files:
        tile = load_mesh(file)
        tile = realign_mesh(tile)
        tile = rotate_mesh(tile)
        tile = add_support(tile)
        write_output(tile, file)

