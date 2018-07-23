#!/usr/bin/env python

import os
import yaml
import mock
import pytest
import shutil

from batch_submit_prof import (contur_setup, herwig_setup, gen_batch_command,
                               batch_submit, valid_arguments, get_args)

# Get necessary directory paths
test_dir = os.path.dirname(os.path.abspath(__file__))
base_grid_dir = os.path.join(test_dir, '..' + os.sep)
test_files_dir = os.path.join(test_dir, 'test_files')
# Read in fixtures file
with open(os.path.join(test_files_dir, 'argument_fixtures.yaml'), 'r') as f:
    arguments_examples = yaml.load(f)


class WorkingDirectory:
    """Context manager for changing working directory"""
    def __init__(self, new_directory):
        self.new_directory = os.path.expanduser(new_directory)

    def __enter__(self):
        self.old_directory = os.getcwd()
        os.chdir(self.new_directory)

    def __exit__(self, exc_type, exc_val, exc_tb):
        os.chdir(self.old_directory)


def parse_command(command):
    with mock.patch('sys.argv', command.split(' ')):
        args = get_args()
    return args


def setup_module():
    """Make a test area and mock some command line options"""
    make_test_area('.', os.path.join(test_files_dir, 'GridSetup'))
    command = 'batch_submit_prof.py 1 -m random -s'
    args = parse_command(command)
    with WorkingDirectory(os.path.join(test_files_dir, 'GridSetup')):
        batch_submit(args)


def teardown_module():
    """Clean up test area"""
    shutil.rmtree(os.path.join(test_files_dir, 'GridSetup'))


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


def test_contur_setup_path():
    """Test specified Contur setup path exists"""
    setup_path = os.path.expandvars(contur_setup.lstrip('source '))
    print("Warning: Contur setup script path points to non-existent file!\n"
          + setup_path)
    path_exists = os.path.exists(setup_path)
    assert path_exists


def test_herwig_setup_path():
    """Test specified Herwig setup path exists"""
    setup_path = os.path.expandvars(herwig_setup.lstrip('source '))
    print("Warning: Herwig setup script path points to non-existent file!\n"
          + setup_path)
    path_exists = os.path.exists(setup_path)
    assert path_exists


@pytest.mark.parametrize('fixture', arguments_examples.iteritems())
def test_get_args(fixture):
    system_args = fixture[1]['command'].split(' ')
    with mock.patch('sys.argv', system_args):
        args = get_args()
    for key, item in fixture[1].iteritems():
        if key != 'command':
            if type(item) == int:
                item = str(item)
            assert eval('args.' + key) == item


@pytest.mark.parametrize('fixture', arguments_examples.iteritems())
def test_valid_arguments(fixture):
    system_args = fixture[1]['command'].split(' ')
    with mock.patch('sys.argv', system_args):
        args = get_args()
    if fixture[0].startswith('valid_'):
        valid_args = valid_arguments(args)
        assert valid_args
    else:
        valid_args = valid_arguments(args)
        assert not valid_args


def test_gen_batch_command():
    """Test gen_batch_command produces expected output"""
    terminal_command = 'batch_submit_prof.py 10 --seed 10 -n 500'
    args = parse_command(terminal_command)
    batch_command, _ = gen_batch_command('test_dir', 'test/test_dir', args)
    expected_command = (
        "%s;\n"
        "cd test/test_dir;\n"
        "%s;\n"
        "Herwig read LHC.in;\n"
        "Herwig run LHC.run --seed=10 --tag=runpoint_test_dir --jobs=2 " 
        "--numevents=500;\n"
        % (herwig_setup, contur_setup))
    assert batch_command == expected_command


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
