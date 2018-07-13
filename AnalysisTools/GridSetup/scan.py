# -*- coding: utf-8 -*-
"""
Created on 29/06/18

@author: HarryS
"""

import shutil
import os
import random
import sys
import numpy as np


def copy_tree(source, destination):
    """Copy a directory and all its contents to a new location"""
    source = os.path.abspath(source)
    destination = os.path.abspath(destination)
    for root, dirs, files in os.walk(source):
        for file_name in files:
            abs_path = os.path.join(root, file_name)
            rel_path = os.path.relpath(abs_path, source)
            copy_to_path = os.path.join(destination, rel_path)
            try:
                shutil.copy(abs_path, copy_to_path)
            except IOError:
                os.makedirs(copy_to_path)
                shutil.copy(abs_path, copy_to_path)


def make_directory(path):
    """If directory does not exist, create it."""
    try:
        os.mkdir(path)
    except OSError, os_error:
        if '[Errno 17] File exists' not in str(os_error):
            raise os_error


def read_param_file(file_path):
    """Read one of the produced param.dat files"""
    with open(file_path, 'r') as f:
        raw_params = f.read().strip().split('\n')

    param_dict = {}
    for param in raw_params:
        name, val = param.split(' ')
        param_dict[name] = float(val)
    return param_dict


def write_sampled_points(output_dir):
    """Write where parameter space was sampled to a .txt file"""
    sampled_points = {}
    for root, _, files in os.walk(output_dir):
        for file_name in files:
            if file_name == 'params.dat':
                run_point = os.path.basename(root)
                param_file_dict = read_param_file(
                    os.path.join(root, file_name))
                sampled_points[run_point] = param_file_dict

    variables = [key for key in sorted(param_file_dict)]
    with open(os.path.join(output_dir, 'sampled_points.dat'), 'w') as f:
        # Write headers
        f.write('run_point: \t')
        [f.write(variable + ': \t') for variable in variables]
        f.write("\n")
        # Write data points
        for run_point, param_dict in sorted(sampled_points.items()):
            f.write(run_point + '\t')
            for variable in variables:
                f.write("%.4f \t" % param_dict[variable])
            f.write('\n')


def uniform_sample(ranges, num_points):
    """Sample given ranges uniformly over given ranges."""
    dimensions = len(ranges)
    points_per_dim = round(num_points**(1./dimensions))
    if points_per_dim != num_points**(float(1./dimensions)):
        permission = ''
        while permission.lower() not in ['no', 'yes', 'n', 'y']:
            permission = raw_input("If using uniform mode number of points^"
                                   "(1/dimensions) must be an integer!\n"
                                   "Do you want to use %i points?\n"
                                   "[y/N]: "
                                   % points_per_dim**dimensions)
        if permission.lower() in ['n', 'no']:
            sys.exit()

    param_spaces = []
    for p_range in ranges:
        space = np.linspace(p_range[0], p_range[1], points_per_dim)
        param_spaces.append(space)
    grid = np.meshgrid(*param_spaces)
    coords = [np.reshape(dim, dim.size) for dim in grid]
    return coords


def gen_format_dict(parameters, idx):
    """Create dictionary to use in formatting template run card."""
    format_dict = {}
    for param, info in sorted(parameters.iteritems()):
        format_dict[param] = info['values'][idx]
    return format_dict


def read_param_ranges(param_file):
    """Read parameter ranges from given parameter file,"""
    parameters = {}
    with open(param_file, 'r') as f:
        for line in f:
            if line.strip():
                try:
                    param, min_val, max_val = line.strip().split(' ')
                    parameters[param] = {}
                    parameters[param]['range'] = (float(min_val),
                                                  float(max_val))
                    parameters[param]['values'] = []
                except ValueError:
                    print("Could not read parameter file.\n%s should be a "
                          "space separated data file formatted as:\n"
                          "[param name] [min value] [max value]"
                          % param_file)
                    sys.exit()
    return parameters


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


def run_scan(num_points, template_paths, grid_pack, output_dir='myscan',
             sample_mode='uniform', param_file='param_file.dat', seed=None):
    """
    Run a scan over parameter space defined in param_file.dat using a
    given sampling mode and write relevant run cards and param files.

    Parameters
    ----------

    num_points: int
        Number of points to sample.

    template_paths: list
        List of template files (eg. LHC.in).

    grid_pack: str or None
        Path to directory containing the model grid pack.

    output_dir: str (default = 'myscan')
        Path to output scan results to.

    sample_mode: str ['uniform', 'random'] (default = 'uniform')
        The mode to sample in.
            Uniform: Sample points uniformly within parameter space. The
                     number of points sampled^(1/number of dimensions)
                     must be an integer.
            Random: Randomly sample the parameter space

    param_file: str (default = 'param4D.dat')
        Path to space seperated file containing parameters and their
        value ranges.
        Eg.
            Xm 50 100
            Y1 75 150

    seed: int (default = None)
        Seed for random number generator to get reproducibility.

    """

    check_param_consistency(param_file, template_paths)

    if seed:
        random.seed(seed)

    # Read in run card template files
    templates = {}
    for template_path in template_paths:
        template_name = os.path.basename(template_path)
        with open(template_path, 'r') as f:
            templates[template_name] = f.read()

    # Read in parameter ranges from parameter file
    parameters = {}
    with open(param_file, 'r') as f:
        for line in f:
            if line.strip():
                try:
                    param, min_val, max_val = line.strip().split(' ')
                    parameters[param] = {}
                    parameters[param]['range'] = (float(min_val),
                                                  float(max_val))
                    parameters[param]['values'] = []
                except ValueError:
                    print("Could not read parameter file.\n%s should be a "
                          "space separated data file formatted as:\n"
                          "[param name] [min value] [max value]"
                          % param_file)
                    sys.exit()

    # Generate parameter values depending on sampling mode
    if sample_mode == 'random':
        for param in sorted(parameters):
            for i in range(num_points):
                random_value = random.uniform(*parameters[param]['range'])
                parameters[param]['values'].append(random_value)

    elif sample_mode == 'uniform':
        ranges = []
        for _, param in sorted(parameters.iteritems()):
            ranges.append(param['range'])
        coords = uniform_sample(ranges, num_points)
        for idx, param in enumerate(sorted(parameters)):
            parameters[param]['values'] = coords[idx]
        num_points = len(coords[0])

    make_directory(output_dir)
    for run_point in range(num_points):
        # If runpoint directories don't exist, make them
        run_point_dir_name = "%04i" % run_point
        run_point_path = os.path.join(output_dir, run_point_dir_name)
        make_directory(run_point_path)

        # Write params.dat file
        run_point_param_file_path = os.path.join(run_point_path, 'params.dat')
        with open(run_point_param_file_path, 'w') as run_point_param_file:
            for param, info in sorted(parameters.iteritems()):
                value = info['values'][run_point]
                run_point_param_file.write("%s %e\n" % (param, value))

        # Write run card template files formatted with parameter values
        for template_name in templates:
            raw_template_text = templates[template_name]
            format_dict = gen_format_dict(parameters, run_point)
            try:
                template_text = raw_template_text.format(**format_dict)
            except KeyError:
                print("Error: Parameters in %s do not match the "
                      "parameters in %s."
                      % (param_file, template_path))
            template_path = os.path.join(run_point_path, template_name)
            with open(template_path, 'w') as f:
                f.write(template_text)

        # Copy across all files in GridPack
        if grid_pack:
            copy_tree(grid_pack, run_point_path)

    # Write all sampled points to a .dat file
    write_sampled_points(output_dir)
