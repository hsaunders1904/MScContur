#!/usr/bin/env python

import numpy as np


def get_points(num_points, parameter_space, weight_grid, factor=1, seed=None):
    """
    Sample parameter space with a weighting to sample more points
    around higher confidence levels. Or you can provide a negative
    factor argument to sample around areas with lower confidence
    levels.

    Parameters
    ----------

    num_points: int
        Number of points to sample.

    parameter_space: list of arrays
        List of arrays giving the space of values in each dimension.
        e.g. [np.linspace(min(x), max(x), grid_size),
              np.linspace(min(y), max(y), grid_size)]

    weight_grid: ndarray
        Grid containing weights.

    factor: int, float
        Factor to give to weighting. The higher this number the more
        points will be selected around high weights.

    Returns
    -------

    coords: list of arrays
        Coordinates of sampled points (length of list = number of
        dimensions).
    """
    if seed:
        np.random.seed(seed)

    meshes = np.meshgrid(*parameter_space)
    flat_meshes = [mesh.reshape(mesh.size) for mesh in meshes]

    weights = np.power(weight_grid.reshape(weight_grid.size), factor)
    normalized_weights = weights/np.sum(weights)
    coords = []

    for flat_mesh in flat_meshes:
        coords.append(np.random.choice(flat_mesh, p=normalized_weights,
                                       size=num_points))
    return np.array(coords).T
