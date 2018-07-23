#!/usr/bin/env python

import __builtin__
import os
import pytest
import mock
import shutil
import numpy as np

import scanning_functions as sf


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


def teardown_module():
    """Delete file created during testing"""
    shutil.rmtree(os.path.join(test_files_dir, 'folder2/'))
    os.remove(os.path.join(test_files_dir, 'folder', 'params.dat'))


def test_copy_tree():
    """Test copy_tree copies top level file and only top level files"""
    source = os.path.join(test_files_dir, 'folder/')
    destination = os.path.join(test_files_dir, 'folder2/')
    sf.copy_tree(source, destination)
    # Get absolute paths of top level items in source directory
    abs_source_files = get_top_level(source)
    # Get all top level item names in destination directory (not full path)
    dest_file_names = os.listdir(destination)
    # Get names of only files in source directory
    source_file_names = []
    for path in abs_source_files:
        if os.path.isfile(path):
            source_file_names.append(os.path.basename(path))
    assert sorted(dest_file_names) == sorted(source_file_names)


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
    """Test read_param_ranges fails when min value greater than max"""
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
    param_dict = sf.read_param_ranges(os.path.join(test_files_dir, 'folder',
                                                   'test_file_1'))
    points_to_gen = 10
    param_dict, _ = sf.generate_points(points_to_gen, 'random', param_dict)
    point_idx = 5
    output_path = os.path.join(test_files_dir, 'folder', 'params.dat')
    sf.write_param_file(param_dict, os.path.join(test_files_dir, 'folder'),
                        point_idx)
    with open(output_path, 'r') as f:
        contents = f.read()
    expected_contents_list = []
    for i in range(1, 5):
        expected_contents_list.append(
            'param%i %e' %(i, param_dict['param%i' % i]['values'][point_idx]))
    expected_contents = '\n'.join(expected_contents_list) + '\n'
    assert contents == expected_contents


def test_generate_points_random_ranges():
    """Test generate_points with random  gens points within ranges"""
    param_dict = sf.read_param_ranges(os.path.join(test_files_dir, 'folder',
                                                   'test_file_1'))
    num_points = 8
    param_dict, _ = sf.generate_points(num_points, 'random', param_dict)
    for param, info in param_dict.iteritems():
        for value in info['values']:
            assert info['range'][0] <= value <= info['range'][1]


def test_generate_points_random_num_points():
    """Test generate_points with random returns correct number of points"""
    param_dict = sf.read_param_ranges(os.path.join(test_files_dir, 'folder',
                                                   'test_file_1'))
    num_points = 8
    _, num_points_2 = sf.generate_points(num_points, 'random', param_dict)
    assert num_points == num_points_2


def test_generate_points_uniform_ranges():
    """Test generate_points with uniform gens points within ranges"""
    param_dict = sf.read_param_ranges(os.path.join(test_files_dir, 'folder',
                                                   'test_file_1'))
    num_points = 16
    param_dict, _ = sf.generate_points(num_points, 'uniform', param_dict)
    for param, info in param_dict.iteritems():
        for value in info['values']:
            assert info['range'][0] <= value <= info['range'][1]


def test_generate_points_uniform_num_points_input():
    """Test generate_points with uniform returns correct number of points"""
    param_dict = sf.read_param_ranges(os.path.join(test_files_dir, 'folder',
                                                   'test_file_1'))
    num_points = 10
    # Create mock object to replace raw_input and return 'yes' when called
    with mock.patch.object(__builtin__, 'raw_input', lambda x: 'yes'):
        _, num_points_2 = sf.generate_points(num_points, 'uniform', param_dict)

    assert num_points_2 == 16


def test_generate_points_uniform_num_points():
    """Test generate_points with uniform returns correct number of points"""
    param_dict = sf.read_param_ranges(os.path.join(test_files_dir, 'folder',
                                                   'test_file_1'))
    num_points = 16
    _, num_points_2 = sf.generate_points(num_points, 'uniform', param_dict)
    assert num_points_2 == num_points
