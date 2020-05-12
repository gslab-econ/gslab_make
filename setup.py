from setuptools import setup, find_packages
from setuptools.command.build_py import build_py

import os
import glob
import shutil


class CleanRepo(build_py):
    """ Build command for cleaning setup directories after installation. """
    
    def run(self):
        # Remove build and dist directories
        if os.path.isdir('build'):
            shutil.rmtree('build')
        if os.path.isdir('dist'):
            shutil.rmtree('dist')
            
        # Remove egg-info and dist-info directories
        egg_info = glob.glob('*.egg-info')
        dist_info = glob.glob('*.dist-info')
        for directory in egg_info + dist_info:
            shutil.rmtree(directory)
                    
setup(cmdclass = {'clean': CleanRepo})