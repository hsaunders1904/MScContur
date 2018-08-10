#!/usr/bin/env python

import sys
import shutil
import os


def copy_tree(source, destination):
    """Copy a directory and its top level contents to a new location"""
    source = os.path.abspath(source)
    if not source.endswith(os.sep):
        source += os.sep
    destination = os.path.abspath(destination)
    if not destination.endswith(os.sep):
        # Paths ending in separator guarantees top level of source copied
        destination += os.sep
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


def gen_format_dict(parameters, idx):
    """Create dictionary to use in formatting template run card."""
    format_dict = {}
    for param, info in sorted(parameters.iteritems()):
        format_dict[param] = info['values'][idx]
    return format_dict


def write_template_files(templates, param_dict, run_point, run_point_path,
                         param_file):
    """Write template files formatted with parameter values"""
    for template_name in templates:
        raw_template_text = templates[template_name]
        format_dict = gen_format_dict(param_dict, run_point)
        try:
            template_text = raw_template_text.format(**format_dict)
        except KeyError:
            print("Error: Parameters in %s do not match the "
                  "parameters in %s."
                  % (param_file, template_name))
            sys.exit()
        template_path = os.path.join(run_point_path, template_name)
        with open(template_path, 'w') as f:
            f.write(template_text)


class WorkingDirectory:
    """Context manager to temporarily change working directory"""
    def __init__(self, temp_working_directory):
        self.temp_working_directory = os.path.abspath(temp_working_directory)

    def __enter__(self):
        self.working_directory = os.getcwd()
        os.chdir(self.temp_working_directory)

    def __exit__(self, exc_type, exc_val, exc_tb):
        os.chdir(self.working_directory)
