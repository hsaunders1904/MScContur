#!/usr/bin/env python

import itertools
import numpy as np
import matplotlib.pyplot as plt

from contur.contur_grid import ConturGrid


def find_next_prime(n):
    """
    Find the next highest prime above n.

    A. Dong, next_prime.py, (2014), GitHubGist Repository:
        https://gist.github.com/ldong/808d5403c5e3b19f2f05
    """
    return find_prime_in_range(n, 2*n)


def find_prime_in_range(a, b):
    """
    Find smallest prime between a and b

    A. Dong, next_prime.py, (2014), GitHubGist Repository:
        https://gist.github.com/ldong/808d5403c5e3b19f2f05
    """
    for p in range(a, b):
        for i in range(2, p):
            if p % i == 0:
                break
        else:
            return p
    return None


def get_cell_centres(cell_edges):
    """From given cell edges calculate the cell centres"""
    cell_centres = [np.zeros(len(edge) - 1) for edge in cell_edges]
    for i, edge in enumerate(cell_edges):
        centres = []
        for j in range(len(edge) - 1):
            centres.append((edge[j] + edge[j + 1]) / 2)
        cell_centres[i] = centres
    return cell_centres


def get_cells_per_dimension(old_points, num_new_points, ranges):
    """Calculate the number of cells per dimension that are needed"""
    dimensions = len(ranges)
    # Number of bins needed to fit the new points so there's one point per bin
    cells_needed = int((len(old_points) + num_new_points)**(1./dimensions))
    # We want this to be prime so, if this is run again, new points won't lie
    # on the boundaries of the cells
    cells_per_dim = find_next_prime(2*cells_needed)
    return cells_per_dim


def get_cell_weights(map_file_path, cells_per_dim, cl_focus):
    """Get cell weightings for ndhistogram from CLs"""
    contur_grid = ConturGrid(map_file_path, cells_per_dim)
    cell_weights = contur_grid.grid
    # Set all weights below cl_focus to zero
    where_greater_than_cl = np.greater(cell_weights, cl_focus)
    cell_weights[where_greater_than_cl] = 0
    # Set all nan values to mean weight
    nan_indices = np.isnan(cell_weights)
    cell_weights[nan_indices] = np.mean(cell_weights[~nan_indices])
    return cell_weights


def get_points(old_points, num_new_points, ranges, cell_weights=None,
               weighting_scale=0.66):
    """
    Generate new points in a multi-dimensional parameter space. Use bins
    to avoid to clustering of points. Each bin/cell is given a weighting
    which is reduced if neighbouring bins/cells get filled with points.
    Bins containing points have a zero weighting.

    Parameters
    ----------

    old_points: ndarray
        Array with shape (Nxm) where N is number of points and m is
        number of dimensions.

    num_new_points: int
        The number of new points to generate.

    ranges: list
        List of tuples specify min and max value for each dimension.

    cell_weights: ndarray (optional)
        Weights to give to each histogram bin/cell. This must have the same
        shape as 'old_points'.

    weighting_scale: float (optional)
        The factor to reduce weights by when a point is sampled nearby. This
        avoids clustering of generated points.

    Returns
    -------

    new_points: ndarray
        Mxn Numpy array where M is 'num_new_points' and n is the number of
        dimensions.

    """
    dims = len(ranges)
    if cell_weights is None:
        cells_per_dim = get_cells_per_dimension(old_points, num_new_points,
                                                ranges)
        num_cells = [cells_per_dim for _ in range(dims)]
        cell_weights = np.ones(num_cells)
    else:
        num_cells = cell_weights.shape

    points = old_points
    new_points = []
    for _ in range(num_new_points):
        # Create nd histogram giving point frequency in each bin
        hist, cell_edges = np.histogramdd(points, num_cells, ranges)

        # Boolean matrix with element true if there's no point in corresponding
        # cell
        empty_cells = np.equal(hist, np.zeros(hist.shape))

        # Get centre of bins
        cell_centres = get_cell_centres(cell_edges)

        # Give 0 weight to bins in which there are already point(s)
        cell_weights = np.where(empty_cells, cell_weights,
                                np.zeros(cell_weights.shape))
        # Get index with largest weighting
        max_idx = np.unravel_index(np.argmax(cell_weights), cell_weights.shape)

        # Keep track of new point and append it to old points as well
        new_point = np.array([c[idx] for idx, c in zip(max_idx, cell_centres)])
        new_points.append(new_point)
        points = np.vstack((points, new_point))

        # Find neighbouring bins and reduce their weighting to avoid clustering
        # This is done by looping over each permutation of idx-1, idx, idx+1 in
        # each dimension.
        neighbouring_idxs = []
        rs = [list(range(i - 1, i + 2)) for i in max_idx]
        for idxs in itertools.product(*rs):
            neighbouring_idxs.append(idxs)
        for idx in neighbouring_idxs:
            # Try block needed here for index error due to boundary bins/cells
            try:
                cell_weights[idx] *= weighting_scale
            except IndexError:
                pass

    return np.array(new_points)
