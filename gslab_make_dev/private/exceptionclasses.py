#! /usr/bin/env python
from __future__ import absolute_import, division, print_function, unicode_literals
from builtins import (bytes, str, open, super, range,
                      zip, round, input, int, pow, object)


class CustomError(Exception):
    def __init__(self, value):
        self.value = value
        
    def __str__(self):
        return repr(self.value)

class CritError(CustomError):
    pass

class SyntaxError(CustomError):
    pass

class LogicError(CustomError):
    pass

    