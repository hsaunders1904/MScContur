#!/usr/bin/env python

import pickle
import numpy as np
from collections import defaultdict

from contur.contur_grid import ConturGrid
from os_functions import *


def permission_to_continue(message):
    """Get permission to continue program"""
    permission = ''
    while permission.lower() not in ['no', 'yes', 'n', 'y']:
        permission = raw_input(message + '\n[y/N]: ')
    if permission.lower() in ['n', 'no']:
        return False
    else:
        return True


def read_template_files(template_paths):
    """Read in template files and store contents in dictionary"""
    templates = {}
    for template_path in template_paths:
        template_name = os.path.basename(template_path)
        with open(template_path, 'r') as f:
            templates[template_name] = f.read()
    return templates


def check_param_consistency(param_file, template_paths):
    """Check that parameters in param file match those in templates."""
    parameters_dict = read_param_ranges(param_file)
    for template_path in template_paths:
        with open(template_path, 'r') as template_file:
            template_text = template_file.read()

        for param in parameters_dict:
            if "{" + param + "}" not in template_text:
                print("ParameterError:\n"
                      "Parameters in %s do not match parameters in %s"
                      % (param_file, template_path))
                sys.exit()


def uniform_sample(ranges, num_points):
    """Sample given ranges uniformly."""
    dimensions = len(ranges)
    points_per_dim = round(num_points ** (1. / dimensions))
    if not np.isclose(points_per_dim, num_points ** (float(1. / dimensions))):
        permission_message = ("If using uniform mode number of points^"
                              "(1/dimensions) must be an integer!\n"
                              "Do you want to use %i points?"
                              % points_per_dim ** dimensions)
        if not permission_to_continue(permission_message):
            sys.exit()
    param_spaces = []
    for param_range in ranges:
        space = np.linspace(param_range[0], param_range[1], points_per_dim)
        param_spaces.append(space)
    grid = np.meshgrid(*param_spaces)
    coords = [np.reshape(dim, dim.size) for dim in grid]
    return coords


def sample_random_weighted(num_points, parameter_space, cl_grid, factor=1,
                           seed=None):
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

    cl_grid: ndarray
        Grid containing confidence levels.

    factor: int, float
        Factor to give to weighting. The higher this number the more
        points will be selected around high confidence levels.

    Returns
    -------

    coords: list of arrays
        Coordinates of sampled points (length of list = number of
        dimensions).
    """
    if seed:
        np.random.seed(seed)

    meshes = np.meshgrid(*parameter_space)
    print len(meshes)
    flat_meshes = [mesh.reshape(mesh.size) for mesh in meshes]

    weights = np.power(cl_grid.reshape(cl_grid.size), factor)
    normalized_weights = weights/np.sum(weights)
    coords = []
    for flat_mesh in flat_meshes:
        coords.append(np.random.choice(flat_mesh, p=normalized_weights,
                                       size=num_points))
    return coords


def generate_points(num_points, mode, param_dict, map_file=None):

    if mode == 'random':
        for param, info in sorted(param_dict.iteritems()):
            random_vals = np.random.uniform(info['range'][0], info['range'][1],
                                            size=num_points)
            param_dict[param]['values'] = random_vals

    elif mode == 'uniform':
        ranges = []
        for _, param in sorted(param_dict.iteritems()):
            ranges.append(param['range'])
        coords = uniform_sample(ranges, num_points)
        for idx, param in enumerate(sorted(param_dict)):
            param_dict[param]['values'] = coords[idx]
        num_points = len(coords[0])

    elif mode == 'weighted':
        with open(map_file, 'rb') as f:
            point_list = pickle.load(f)

        old_parameter_vals = defaultdict(list)
        combined_CLs = []
        for point in point_list:
            for param, value in point.params.iteritems():
                old_parameter_vals[param].append(value)
            combined_CLs.append(point.conturPoint.CLs)

        parameter_list = [param for param in param_dict]

        contur_grid = ConturGrid(map_file, 300, parameter_list)

        coords = sample_random_weighted(num_points, contur_grid.parameter_space,
                                        contur_grid.grid)

        for idx, param in enumerate(sorted(param_dict)):
            param_dict[param]['values'] = coords[idx]

    return param_dict, num_points




