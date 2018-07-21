#!/usr/bin/env python

import os
import yaml
import pytest
import shutil

from batch_submit_prof import (contur_setup, herwig_setup, gen_batch_command,
                               batch_submit, valid_arguments)

# Get necessary directory paths
test_dir = os.path.dirname(os.path.abspath(__file__))
base_grid_dir = os.path.join(test_dir, '..' + os.sep)
test_files_dir = os.path.join(test_dir, 'test_files')

with open(os.path.join(test_files_dir, 'argument_fixtures.yaml'), 'r') as f:
    arguments_examples = yaml.load(f)


class ArgsMock:
    """Class to mimic arguments object produced by argparse"""
    def __init__(self, num_points, sample_mode='uniform', out_dir='myscan',
                 param_file='param_file.dat', template_files=['LHC.in'],
                 grid_pack='GridPack', num_events='10000', seed=None,
                 scan_only=False):
        self.num_points = num_points
        self.sample_mode =sample_mode
        self.out_dir = out_dir
        self.param_file = param_file
        self.template_files = template_files
        self.grid_pack = grid_pack
        self.num_events = num_events
        self.seed = seed
        self.scan_only = scan_only


def convert_fixture_to_mock_args(fixture):
    args_mock = ArgsMock(
        fixture['num_points'],
        fixture['sample_mode'],
        fixture['out_dir'],
        fixture['param_file'],
        fixture['templates'],
        fixture['grid'],
        fixture['numevents'],
        fixture['seed'],
        fixture['scan_only'])
    return args_mock


@pytest.mark.parametrize('fixture', arguments_examples.iteritems())
def test_valid_arguments(fixture):
    args = convert_fixture_to_mock_args(fixture[1])
    if fixture[0] == 'default':
        try:
            valid_args = valid_arguments(args)
            assert valid_args
        except AssertionError:
            pytest.fail("Default command line options invalid!")
        except Exception, exception:
            print(exception)
            pytest.fail("Default command line options throws Exception!")
    else:
        valid_args = valid_arguments(args)
        assert not valid_args


def make_test_area(source, destination):
    """Copy GridSetup to new location to run tests with"""
    for root, dirs, files in os.walk(source):
        for file_name in sorted(files):
            path = os.path.join(root, file_name)
            condition = 'myscan' in path or 'tests' in path
            if not condition:
                abs_path = os.path.join(root, file_name)
                rel_path = os.path.relpath(abs_path, source)
                copy_to_path = os.path.join(destination, rel_path)
                try:
                    shutil.copy(abs_path, copy_to_path)
                except IOError:
                    os.makedirs(os.path.dirname(copy_to_path))
                    shutil.copy(abs_path, copy_to_path)


def setup_module():
    """Make a test area and mock some command line options"""
    make_test_area('.', os.path.join(test_files_dir, 'GridSetup'))
    args = ArgsMock(1, sample_mode='random', scan_only=True)
    os.chdir(os.path.join(test_files_dir, 'GridSetup'))
    try:
        batch_submit(args)
    except Exception, exception:
        os.chdir(base_grid_dir)
        raise exception
    os.chdir(base_grid_dir)


def teardown_module():
    """Clean up test area"""
    shutil.rmtree(os.path.join(test_files_dir, 'GridSetup'))


def test_contur_setup_path():
    """Test specified Contur setup path exists"""
    setup_path = contur_setup.lstrip('source ').replace('$HOME',
                                                        os.environ['HOME'])
    print("Warning: Contur setup script path points to non-existent file!\n"
          + setup_path)
    path_exists = os.path.exists(setup_path)
    assert path_exists


def test_herwig_setup_path():
    """Test specified Herwig setup path exists"""
    setup_path = herwig_setup.lstrip('source ').replace('$HOME',
                                                        os.environ['HOME'])
    print("Warning: Herwig setup script path points to non-existent file!\n"
          + setup_path)
    path_exists = os.path.exists(setup_path)
    assert path_exists


def test_gen_batch_command():
    """Test gen_batch_command produces expected output"""
    args = ArgsMock(10, seed=10, num_events='500')
    command, _ = gen_batch_command('test_dir', 'test/test_dir', args)
    expected_command = (
        "%s;\n"
        "cd test/test_dir;\n"
        "%s;\n"
        "Herwig read LHC.in;\n"
        "Herwig run LHC.run --seed=10 --tag=runpoint_test_dir --jobs=2 " 
        "--numevents=500;\n"
        % (herwig_setup, contur_setup))
    assert command == expected_command


def test_batch_submit_grid_pack():
    """Test all files in grid pack are copied to run point directory"""
    grid_pack_files = [f for f in os.listdir('GridPack') if os.path.isfile(f)]
    os.chdir(os.path.join(test_files_dir, 'GridSetup'))
    try:
        scan_dir_files = [f for f in os.listdir('myscan/0000/')]
    finally:
        os.chdir(base_grid_dir)
    for grid_pack_file in grid_pack_files:
        assert grid_pack_file in scan_dir_files


def test_batch_submit_param_file():
    """Test batch submit produces param file in run point directory"""
    os.chdir(os.path.join(test_files_dir, 'GridSetup'))
    try:
        param_file_exists = os.path.exists('myscan/0000/params.dat')
    finally:
        os.chdir(base_grid_dir)
    assert param_file_exists


def test_batch_submit_template_file():
    """Test template file is copied to run point directory"""
    os.chdir(os.path.join(test_files_dir, 'GridSetup'))
    try:
        template_file_exists = os.path.exists('myscan/0000/LHC.in')
    finally:
        os.chdir(base_grid_dir)
    assert template_file_exists

