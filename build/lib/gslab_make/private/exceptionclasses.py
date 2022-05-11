# -*- coding: utf-8 -*-
from builtins import (bytes, str, open, super, range,
                      zip, round, input, int, pow, object)

import sys
import codecs

from termcolor import colored
import colorama
colorama.init()

import gslab_make.private.metadata as metadata

"""
For some fixes Exception printing and I have no idea why...
"""

import subprocess
process = subprocess.Popen('', shell = True)
process.wait()


class CritError(Exception):
    pass

class ColoredError(Exception):
    """Colorized error messages."""
    
    def __init__(self, message = '', trace = ''):
        if message:
            message = '\n\n' + colored(message, color = metadata.color_failure)  
        if trace:
            message += '\n\n' + colored(trace, color = metadata.color_failure)
        
        super(ColoredError, self).__init__(message)
            
class ProgramError(ColoredError):
    """Program execution exception."""
    
    pass