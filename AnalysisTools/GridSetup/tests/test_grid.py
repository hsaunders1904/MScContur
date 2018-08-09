#!/usr/bin/env python

import os
import pytest

from contur.Scanning.scan import read_param_ranges


def test_grid_pack_exists():
    """Test GridPack directory exists"""
    grid_pack_exists = os.path.isdir('GridPack')
    if not grid_pack_exists:
        print("Warning: No 'GridPack' directory!")
    assert grid_pack_exists


def test_grid_pack_model_exists():
    """Check grid pack contatins FRModel.model"""
    if not os.path.exists('GridPack/FRModel.model'):
        pytest.fail("No FRModel.model file in grid pack!\nHave you run "
                    "ufo2herwig on your model directory?")


def test_grid_pack_model_object_exists():
    """Check grid pack contains FRModel.so"""
    so_file_exists = os.path.exists('GridPack/FRModel.so')
    if not so_file_exists:
        if os.path.exists('GridPack/Makefile'):
            pytest.fail("No FRModel.so file in grid pack!\nDid you run make "
                        "after running ufo2herwig?")
        else:
            pytest.fail("No FRModel.so or Makefile in grid pack!\nWas "
                        "ufo2herwig run successfully?")


def test_param_file():
    """Check parameter file exists and of correct format"""
    valid_param_file = True
    try:
        read_param_ranges('param_file.dat')
    except ValueError, value_error:
        print("Warning: scanning_functions.read_param_ranges broken or "
              "'param_file.dat' not in required format! %s"
              % value_error)
        valid_param_file = False
    except IOError, io_error:
        print("Warning: could not read 'param_file.dat! %s" % str(io_error))
        valid_param_file = False
    assert valid_param_file


def test_param_file_lhc_consistency():
    """Test parameters present in both param file and LHC.in"""
    consistent_variables = True
    params = read_param_ranges('param_file.dat')
    with open('LHC.in', 'r') as f:
        lhc_in = f.read()

    parameter_dict = {}
    for param in params:
        parameter_dict[param] = 1
    try:
        lhc_in.format(**parameter_dict)
    except KeyError, key_error:
        print("Warning: Parameter %s present in 'LHC.in' but not present in "
              "'params_file.dat'." % str(key_error))
        consistent_variables = False

    for param in params:
        if param not in lhc_in:
            print("Warning: parameter '%s' present in 'param_file.dat' but not"
                  " in 'LHC.in'." % param)
            consistent_variables = False
    assert consistent_variables
