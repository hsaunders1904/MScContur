#!/usr/bin/env python

import sys
import numpy as np
import shutil
import os
import random


def copy_tree(source, destination):
    """Copy a directory and its top level contents to a new location"""
    source = os.path.abspath(source)
    if not source.endswith(os.sep):
        source += os.sep
    destination = os.path.abspath(destination)
    if not destination.endswith(os.sep):
        destination += os.sep
    # Making sure paths end in separator guarantees top level of source copied
    for root, dirs, files in os.walk(source):
        for file_name in files:
            abs_path = os.path.join(root, file_name)
            rel_path = os.path.relpath(abs_path, source)
            copy_to_path = os.path.join(destination, rel_path)
            try:
                shutil.copy(abs_path, copy_to_path)
            except IOError:
                os.makedirs(os.path.dirname(copy_to_path))
                shutil.copy(abs_path, copy_to_path)
        break


def make_directory(path):
    """If directory does not exist, create it."""
    try:
        os.mkdir(path)
    except OSError, os_error:
        if '[Errno 17] File exists' not in str(os_error):
            raise os_error


def read_param_file(file_path):
    """Read one of the produced params.dat files"""
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


def permission_to_continue(message):
    """Get permission to continue program"""
    permission = ''
    while permission.lower() not in ['no', 'yes', 'n', 'y']:
        permission = raw_input(message)
    if permission.lower() in ['n', 'no']:
        return False
    else:
        return True


def uniform_sample(ranges, num_points):
    """Sample given ranges uniformly."""
    dimensions = len(ranges)
    points_per_dim = round(num_points ** (1. / dimensions))
    if not np.isclose(points_per_dim, num_points ** (float(1. / dimensions))):
        permission_message = ("If using uniform mode number of points^"
                              "(1/dimensions) must be an integer!\n"
                              "Do you want to use %i points?\n"
                              "[y/N]: "
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
                    if float(min_val) >= float(max_val):
                        raise ValueError("Maximum value must be greater than "
                                         "minimum in parameter file: %s"
                                         % param_file)
                    parameters[param] = {}
                    parameters[param]['range'] = (float(min_val),
                                                  float(max_val))
                    parameters[param]['values'] = []
                except ValueError, value_error:
                    if "Maximum value" in str(value_error):
                        raise value_error
                    else:
                        raise ValueError(
                            "Could not read parameter file.\n%s should be a "
                            "space separated data file formatted as:\n"
                            "[param name] [min value] [max value]"
                            % param_file)
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


def read_template_files(template_paths):
    """Read in template files and store contents in dictionary"""
    templates = {}
    for template_path in template_paths:
        template_name = os.path.basename(template_path)
        with open(template_path, 'r') as f:
            templates[template_name] = f.read()
    return templates


def generate_points(num_points, mode, param_dict):
    """Generate points in parameter space via given mode"""
    if mode == 'random':
        for param in sorted(param_dict):
            for i in range(num_points):
                random_value = random.uniform(*param_dict[param]['range'])
                param_dict[param]['values'].append(random_value)

    elif mode == 'uniform':
        ranges = []
        for _, param in sorted(param_dict.iteritems()):
            ranges.append(param['range'])
        coords = uniform_sample(ranges, num_points)
        for idx, param in enumerate(sorted(param_dict)):
            param_dict[param]['values'] = coords[idx]
        num_points = len(coords[0])

    return param_dict, num_points


def make_run_point_directory(run_point, output_dir):
    """If runpoint directories don't exist, make them and return path"""
    run_point_dir_name = "%04i" % run_point
    run_point_path = os.path.join(output_dir, run_point_dir_name)
    make_directory(run_point_path)
    return run_point_path


def write_param_file(param_dict, run_point_path, run_point):
    """Write param file containing parameter values for given run point"""
    run_point_param_file_path = os.path.join(run_point_path, 'params.dat')
    with open(run_point_param_file_path, 'w') as run_point_param_file:
        for param, info in sorted(param_dict.iteritems()):
            value = info['values'][run_point]
            run_point_param_file.write("%s %e\n" % (param, value))


def write_template_files(templates, param_dict, run_point, run_point_path,
                         param_file):
    """Write template files formatted with """
    for template_name in templates:
        raw_template_text = templates[template_name]
        format_dict = gen_format_dict(param_dict, run_point)
        try:
            template_text = raw_template_text.format(**format_dict)
        except KeyError:
            print("Error: Parameters in %s do not match the "
                  "parameters in %s."
                  % (param_file, template_path))
        template_path = os.path.join(run_point_path, template_name)
        with open(template_path, 'w') as f:
            f.write(template_text)
