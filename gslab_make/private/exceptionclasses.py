#! /usr/bin/env python
from __future__ import absolute_import, division, print_function, unicode_literals
from builtins import (bytes, str, open, super, range,
                      zip, round, input, int, pow, object)

import sys
import codecs

from termcolor import colored
import colorama
colorama.init()

import gslab_make.private.metadata as metadata

def decode(string):
    """Decode string."""

    if (sys.version_info < (3, 0)):
        # string = codecs.decode(string, 'utf-8') 
        string = string.decode(encoding = 'utf-8', errors = 'ignore')
    return(string)


def encode(string):
    """Clean string for encoding."""

    if (sys.version_info < (3, 0)):
        string = codecs.encode(string, 'utf-8')  

    return(string)


class CritError(Exception):
    pass

class ColoredError(Exception):
    """Colorized error messages."""
    
    def __init__(self, message = '', trace = ''):
        if message:
            message = decode(message)
            message = '\n\n' + colored(message, color = metadata.color_failure)  
        if trace:
            trace = decode(trace)
            message += '\n\n' + colored(trace, color = metadata.color_failure)
        
        super(ColoredError, self).__init__(encode(message))
            
class ProgramError(ColoredError):
    """Program execution exception."""
    
    pass