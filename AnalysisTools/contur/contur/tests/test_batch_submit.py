#!/usr/bin/env python

import os
import yaml
import mock
import pytest
import shutil

from contur.Scanning.batch_submit import \
    (gen_batch_command, batch_submit, valid_arguments, get_args)

# Get necessary directory paths
test_dir = os.path.dirname(os.path.abspath(__file__))
base_grid_dir = os.path.abspath(os.path.join(test_dir, '../../../GridSetup'))
test_files_dir = os.path.join(test_dir, 'test_files')

# Read in fixtures file
with open(os.path.join(test_files_dir, 'argument_fixtures.yaml'), 'r') as f:
    arguments_examples = yaml.load(f)

# These do not need to be real paths, they're just to check they're written
# correctly to batch shell script
setup_commands = {
    'Herwig': "source .../Herwig-Tip/setupEnv.sh",
    'Contur': "source .../contur/setupContur.sh"}


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
    """Parse given command using parser in 'batch_submit.py'"""
    with mock.patch('sys.argv', command.split(' ')):
        args = get_args()
    return args


def make_test_area(source, destination):
    """Copy GridSetup to new location to run tests with"""
    for root, dirs, files in os.walk(source):
        for file_name in sorted(files):
            path = os.path.join(root, file_name)
            condition = [
                name in path for name in
                    ['tests', 'Legacy', '__', 'myscan', 'README']]
            if not any(condition):
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
    make_test_area(base_grid_dir, os.path.join(test_files_dir, 'GridSetup'))
    command = 'batch_submit.py 1 -m random -s'
    args = parse_command(command)
    with WorkingDirectory(os.path.join(test_files_dir, 'GridSetup')):
        valid_arguments(args)
        batch_submit(args, setup_commands)


@pytest.mark.parametrize('fixture', arguments_examples.iteritems())
def test_get_args(fixture):
    """Test that each flag/option in parser returns expected values"""
    system_args = fixture[1]['command'].split(' ')
    with mock.patch('sys.argv', system_args):
        args = get_args()
    for key, item in fixture[1].iteritems():
        if key != 'command':
            if type(item) == int:
                item = str(item)
            print key, '=', getattr(args, key), type(getattr(args, key))
            if getattr(args, key) != item:
                pytest.fail(
                    'Failed on: ' + key + '\n' +
                    'args.' + key + ' is not ' + str(item))


@pytest.mark.parametrize('fixture', arguments_examples.iteritems())
def test_valid_arguments(fixture):
    """
    Test that 'valid_arguments' function recognises valid and invalid
    args
    """
    system_args = fixture[1]['command'].split(' ')
    with mock.patch('sys.argv', system_args):
        args = get_args()
    with WorkingDirectory(base_grid_dir):
        if fixture[0].startswith('valid_'):
            valid_args = valid_arguments(args)
            assert valid_args
        else:
            valid_args = valid_arguments(args)
            assert not valid_args


def test_gen_batch_command():
    """Test gen_batch_command produces expected output"""
    terminal_command = 'batch_submit.py 10 --seed 10 -n 500 -t LHC-trial.in'
    args = parse_command(terminal_command)
    batch_command, _ = gen_batch_command('test_dir', 'test/test_dir', args,
                                         setup_commands)
    expected_command = (
        "{Herwig};\n"
        "{Contur};\n"
        "cd test/test_dir;\n"
        "Herwig read LHC-trial.in;\n"
        "Herwig run LHC-trial.run --seed=10 --tag=runpoint_test_dir --jobs=2 " 
        "--numevents=500;\n".format(**setup_commands))
    assert batch_command == expected_command


def test_batch_submit_grid_pack():
    """Test all files in grid pack are copied to run point directory"""
    with WorkingDirectory(os.path.join(test_files_dir, 'GridSetup')):
        grid_pack_files = [
            f for f in os.listdir('GridPack') if os.path.isfile(f)]
        scan_dir_files = [
            f for f in os.listdir('myscan00/0000/')]
        for grid_pack_file in grid_pack_files:
            assert grid_pack_file in scan_dir_files


def test_batch_submit_param_file():
    """Test batch submit produces param file in run point directory"""
    with WorkingDirectory(os.path.join(test_files_dir, 'GridSetup')):
        param_file_exists = os.path.exists('myscan00/0000/params.dat')
        assert param_file_exists


def test_batch_submit_template_file():
    """Test template file is copied to run point directory"""
    with WorkingDirectory(os.path.join(test_files_dir, 'GridSetup')):
        template_file_exists = os.path.exists('myscan00/0000/LHC.in')
        assert template_file_exists


def teardown_module():
    """Clean up test area"""
    shutil.rmtree(os.path.join(test_files_dir, 'GridSetup'))
