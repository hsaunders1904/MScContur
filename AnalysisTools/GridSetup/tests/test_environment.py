#!/usr/bin/env python

import pytest
import subprocess
import os
import sys
import platform
from subprocess import CalledProcessError

herwig_directory = '/unix/cedar/software/sl6/Herwig-Tip/'
try:
    contur_directory = os.environ['$CONTURMODULEDIR']
except KeyError:
    contur_directory = os.path.join('$HOME', 'contur')


def test_herwig_environment():
    """Test Herwig can be called from shell"""
    try:
        a = subprocess.check_output(['Herwig --version'], shell=True)
        print(a)
    except CalledProcessError:
        pytest.fail("Error calling Herwig!\nIs your environment set up "
                    "correctly?")


def test_python_version():
    """Test python is python 2"""
    python_version = sys.version[:3]
    if python_version > '2.7':
        pytest.fail("Python version error!\nYou must use a version <= 2.7.")


def test_python_path():
    """Test python path includes Contur and Herwig directories"""
    try:
        python_path = os.environ['PYTHONPATH'].split(':')

        required_paths = [os.path.join(contur_directory, 'AnalysisTools',
                                       'contur'),
                          os.path.join(herwig_directory, 'lib64', 'python2.7',
                                       'site-packages')]
        for required_path in required_paths:
            if required_path not in python_path:
                pytest.fail("'%s' not in python path" % required_path)
    except KeyError:
        pytest.fail("No PYTHONPATH environment variable!\nYou need to add "
                    "'%s' and '%s' to your python path."
                    % (required_paths[0], required_paths[1]))


def test_bash_path():
    """Test necessary paths are in system path"""
    bash_path = os.environ['PATH'].split(':')
    required_paths = [
        os.path.join(contur_directory, 'AnalysisTools', 'contur', 'bin'),
        os.path.join(herwig_directory, 'bin'),
        os.path.abspath('/unix/cedar/software/sl6/python/bin'),
        os.path.abspath('/opt/rh/python27/root/usr/bin'),
        os.path.abspath('/opt/rh/devtoolset-4/root/usr/bin')]
    for required_path in required_paths:
        if required_path not in bash_path:
            pytest.fail("'%s' not in system path!" % required_path)


def test_platform():
    """Check platform of PC matches batch farm platform"""
    flag = False
    try:
        with open('/etc/redhat-release', 'r') as f:
            redhat_release = f.read().strip()
        if 'Scientific Linux' not in redhat_release:
            flag = True
    except(IOError, OSError):
            os_platform = platform.platform(aliased=True)
            if 'redhat' not in os_platform and 'Carbon' not in os_platform:
                flag = True
    if flag:
        pytest.fail("The OS on this PC may not match the OS on the batch farm."
                    "\nThis may cause errors when the farm tries to run "
                    "executables compiled on this PC.")
