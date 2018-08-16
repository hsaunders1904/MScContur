#!/usr/bin/env python

import __builtin__
import os
import pytest
import mock
import numpy as np

import contur.Scanning.scanning_functions as sf
from contur.Scanning.batch_submit import get_args


def move_up_dirs(path, levels):
    """Move up given number of diretory levels"""
    return os.path.abspath(os.path.join(path, ('..'+os.sep)*levels))


# Get necessary directory paths
test_dir = os.path.dirname(os.path.abspath(__file__))
base_grid_dir = move_up_dirs(test_dir, 2)
test_files_dir = os.path.join(test_dir, 'test_files')


def get_top_level(path):
    """Get top level files and directories in given directory"""
    return [os.path.join(path, item) for item in os.listdir(path)]


def test_read_param_ranges_valid():
    """Test read_param_ranges successful on valid param file"""
    param_file_1 = os.path.join(test_files_dir, 'folder', 'test_file_1')
    params = sf.read_param_ranges(param_file_1)
    expected_params = {'param1': {'range': (0, 1), 'values': []},
                       'param2': {'range': (10, 100), 'values': []},
                       'param3': {'range': (4, 10), 'values': []},
                       'param4': {'range': (0, 1), 'values': []}}
    assert params == expected_params


def test_read_param_ranges_invalid():
    """Test read_param_ranges fails on an invalid param file"""
    param_file_2 = os.path.join(test_files_dir, 'folder', 'test_file_2')
    with pytest.raises(ValueError):
        sf.read_param_ranges(param_file_2)


def test_read_param_ranges_min_greater_than_max():
    """Test read_param_ranges fails when min value greater or equal to max"""
    param_file_3 = os.path.join(test_files_dir, 'folder', 'folder_depth_2',
                                'test_file_3')
    with pytest.raises(ValueError):
        sf.read_param_ranges(param_file_3)


def test_uniform_sample():
    """Test uniform sample gives correct output"""
    ranges = [[0, 10], [2, 4], [5, 10]]
    num_points = 8
    coords = sf.uniform_sample(ranges, num_points)
    assert len(coords[0]) == num_points
    assert len(coords) == len(ranges)
    expected_coords = np.array([
        np.array([0, 0, 10, 10, 0, 0, 10, 10]),
        np.array([2, 2, 2, 2, 4, 4, 4, 4]),
        np.array([5, 10, 5, 10, 5, 10, 5, 10])], dtype=float)
    print("Warning: Coordinates not equal to those expected!")
    assert np.array(coords).all() == np.array(expected_coords).all()


def test_read_param_file():
    """Test read param_file reads valid param file correctly"""
    param_dict = sf.read_param_file(os.path.join(test_files_dir, 'params.dat'))
    expected_param_dict = {'gYq': 1,
                           'Xm': 200,
                           'Y1': 400}
    print("Warning: Parameter file incorrectly read!")
    assert param_dict == expected_param_dict


def test_write_param_file():
    """Test write_param_file writes to file correctly"""
    param_dict = {'Xm': {'range': (100, 2000),
                         'values': [1, 2, 3, 4]},
                  'Y1': {'range': (100, 3000),
                         'values': [5, 6, 7, 8]}}
    point_idx = 3
    output_path = os.path.join(test_files_dir, 'folder', 'params.dat')
    sf.write_param_file(param_dict, os.path.join(test_files_dir, 'folder'),
                        point_idx)

    with open(output_path, 'r') as f:
        contents = f.read().strip()

    expected_contents = "Xm %e\nY1 %e" % \
                        (param_dict['Xm']['values'][point_idx],
                         param_dict['Y1']['values'][point_idx])

    assert contents == expected_contents


def test_generate_points_random_ranges():
    """Test generate_points with random  gens points within ranges"""
    param_dict = sf.read_param_ranges(os.path.join(test_files_dir, 'folder',
                                                   'test_file_1'))
    command = 'batch-submit 16 -m random -s'
    with mock.patch('sys.argv', command.split(' ')):
        args = get_args()

    param_dict, num_points_ = sf.generate_points(args, param_dict)
    for param, info in param_dict.iteritems():
        for value in info['values']:
            assert info['range'][0] <= value <= info['range'][1]


def test_generate_points_random_num_points():
    """Test generate_points with random returns correct number of points"""
    param_dict = sf.read_param_ranges(os.path.join(test_files_dir, 'folder',
                                                   'test_file_1'))
    command = 'batch-submit 16 -m random -s'
    with mock.patch('sys.argv', command.split(' ')):
        args = get_args()

    _, num_points = sf.generate_points(args, param_dict)
    assert num_points == 16


def test_generate_points_uniform_ranges():
    """Test generate_points with uniform gens points within ranges"""
    param_dict = sf.read_param_ranges(os.path.join(test_files_dir, 'folder',
                                                   'test_file_1'))

    command = 'batch-submit 16 -s'
    with mock.patch('sys.argv', command.split(' ')):
        args = get_args()

    param_dict, _ = sf.generate_points(args, param_dict)
    for param, info in param_dict.iteritems():
        for value in info['values']:
            assert info['range'][0] <= value <= info['range'][1]


def test_generate_points_uniform_num_points_input():
    """Test generate_points with uniform returns correct number of points"""
    param_dict = sf.read_param_ranges(os.path.join(test_files_dir, 'folder',
                                                   'test_file_1'))
    command = 'batch-submit 10 -m uniform -s'
    with mock.patch('sys.argv', command.split(' ')):
        args = get_args()

    # Create mock object to replace raw_input and return 'yes' when called
    with mock.patch.object(__builtin__, 'raw_input', lambda x: 'yes'):
        _, num_points = param_dict, _ = sf.generate_points(args, param_dict)

    assert num_points == 16


def test_generate_points_uniform_num_points():
    """Test generate_points with uniform returns correct number of points"""
    param_dict = sf.read_param_ranges(os.path.join(test_files_dir, 'folder',
                                                   'test_file_1'))

    command = 'batch-submit 16 -m uniform -s'
    with mock.patch('sys.argv', command.split(' ')):
        args = get_args()

    _, num_points = sf.generate_points(args, param_dict)

    assert num_points == 16


def teardown_module():
    """Delete file created during testing"""
    os.remove(os.path.join(test_files_dir, 'folder', 'params.dat'))
