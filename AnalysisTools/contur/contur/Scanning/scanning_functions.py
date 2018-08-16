#!/usr/bin/env python

import pickle
import numpy as np

from contur.contur_grid import ConturGrid
from contur.Scanning import weighted_bins, weighted_random
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


def read_template_file(template_path):
    """Read in template files and store contents in dictionary"""
    template = {}
    with open(template_path, 'r') as f:
        template[template_path] = f.read()
    return template


def check_param_consistency(param_file, template_path):
    """Check that parameters in param file match those in templates."""
    parameters_dict = read_param_ranges(param_file)
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


def read_old_points(map_file):
    """Read coordinates of points sampled in .map file"""
    with open(map_file, 'rb') as f:
        depots = pickle.load(f)

    points = []
    for depot in depots:
        points.append([depot.params[param] for param in sorted(depot.params)])
    old_points = np.array(points)

    return old_points


def generate_points(args, param_dict):
    """
    Generate points to sample using given mode.

    Parameters
    ----------

    args: argparse.Namespace object
        Namespace object containing values of command line options.

    param_dict: dict
        Dictionary with parameter names as keys each containing another
        dictionary with keys 'range' and 'values'.

     Returns
     -------

     param_dict: dict
        Same param_dict as was passed in to the function but now filled
        with points.

    num_points: int
        The number of points generated.

    """
    if args.mode == 'random':
        # Random coordinates within parameter space
        for param, info in sorted(param_dict.iteritems()):
            random_vals = np.random.uniform(info['range'][0], info['range'][1],
                                            size=args.num_points)
            param_dict[param]['values'] = random_vals

    elif args.mode == 'uniform':
        # Points generated equally spaced throughout parameter space
        ranges = []
        for _, param in sorted(param_dict.iteritems()):
            ranges.append(param['range'])
        coords = uniform_sample(ranges, args.num_points)
        for idx, param in enumerate(sorted(param_dict)):
            param_dict[param]['values'] = coords[idx]
        args.num_points = len(coords[0])

    elif args.mode == 'weighted':
        # Points generated randomly with weights dictated by args.rescan .map
        # file

        # Check the amount of memory the ConturGrid object will use before
        # creating it. Use a coarser grid if memory limit exceeded
        num_dims = len(param_dict)
        mem_limit = 1.6e9  # bits
        grid_size = 300
        if grid_size**num_dims > mem_limit:
            grid_size = int(mem_limit**(1./num_dims))

        contur_grid = ConturGrid(args.map_file, grid_size)

        # Replace any NaNs with the mean CLs in interpolated grid.
        nan_indices = np.isnan(contur_grid.grid)
        contur_grid.grid[nan_indices] = np.mean(contur_grid.grid[~nan_indices])
        new_points = weighted_random.get_points(
            args.num_points, contur_grid.parameter_space, contur_grid.grid.T,
            args.factor, args.cl_focus)
        for idx, param in enumerate(sorted(param_dict)):
            param_dict[param]['values'] = new_points[:, idx]

    elif args.mode == 'bins':
        # Generate points based on bins method
        old_points = read_old_points(args.map_file)
        ranges = []
        for _, param in sorted(param_dict.iteritems()):
            ranges.append(param['range'])

        cells_per_dim = weighted_bins.get_cells_per_dimension(
            old_points, args.num_points, ranges)

        contur_grid = ConturGrid(args.map_file, cells_per_dim)

        new_points = weighted_bins.get_points(
            old_points, args.num_points, ranges, contur_grid.grid, args.factor)

        for idx, param in enumerate(sorted(param_dict)):
            param_dict[param]['values'] = new_points[:, idx]

    return param_dict, args.num_points
