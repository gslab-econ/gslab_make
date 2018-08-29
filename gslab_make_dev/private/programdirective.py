#! /usr/bin/env python
from __future__ import absolute_import, division, print_function, unicode_literals
from builtins import (bytes, str, open, super, range,
                      zip, round, input, int, pow, object)

import os
import subprocess
import shutil

from private.exceptionclasses import CritError
import private.messages as messages
import private.metadata as metadata
from private.utility import norm_path

class Directive(object):

    def __init__(self, 
                 osname = os.name,
                 shell = False,
                 makelog = metadata.settings['makelog'], 
                 log = ''):

        self.osname   = osname
        self.shell    = shell
        self.makelog  = makelog
        self.log      = log  
        self.check_os()
        self.get_paths()

    def check_os(self):
        if (self.osname != 'posix') & (self.osname != 'nt'):
            raise CritError(messages.crit_error_unknown_system % self.osname)

    def get_paths(self):    
        self.makelog  = norm_path(self.makelog)
        self.log      = norm_path(self.log) if self.log != '' else self.log        

    def execute_command(self, command):   
        command = command.split()
        self.output = 'Executing: "' + ' '.join(command) + "'"
        print(self.output)
            
        try:   
             p = subprocess.Popen(command, stdout = subprocess.PIPE, stderr = subprocess.PIPE, shell = self.shell)
             out, err = p.communicate()
             print(err)
             self.output += '\n' + out + '\n' + err
        except Exception as errmsg:
             error_message = messages.crit_error_bad_command % ' '.join(command) + '\n' + str(errmsg)
             print(error_message)
             self.output += '\n' + error_message

    def write_log(self):
        if self.makelog: 
            if not (metadata.makelog_started and os.path.isfile(self.makelog)):
                raise CritError(messages.crit_error_no_makelog % self.makelog)
            with open(self.makelog, 'a') as f:
                f.write(self.output)

        if self.log:
            with open(self.log, 'w') as f:
                f.write(self.output)


class ProgramDirective(Directive):

    def __init__(self, 
                 application, 
                 program,
                 executable = '', 
                 option = '',
                 args = '', 
                 **kwargs):

        super(ProgramDirective, self).__init__(**kwargs)
        self.application = application
        self.program     = program
        self.executable  = executable
        self.option      = option
        self.args        = args      
        self.parse_program()
        self.check_program()
        self.get_executable()
        self.get_option()

    def parse_program(self):
        self.program      = norm_path(self.program)
        self.program_path = os.path.dirname(self.program)
        self.program_base = os.path.basename(self.program)
        self.program_name, self.program_ext = os.path.splitext(self.program_base)

    def check_program(self):
        if not os.path.isfile(self.program):
            raise CritError(messages.crit_error_no_file % self.program)
            
        if self.program_ext != metadata.extensions[self.application]:
            raise CritError(messages.crit_error_extension % self.program)

    def get_executable(self):
        if not self.executable:
            self.executable = metadata.default_executables[self.osname][self.application]

    def get_option(self):
        if not self.option:
            self.option = metadata.default_options[self.osname][self.application]

    def move_program_output(self, program_output, log = ''):
        """
        Certain programs create outputs that need to be moved to appropriate logging files
        """
    
        try:
            program_output = norm_path(program_output)
            with open(program_output, 'r') as f:
                out = f.read()
        except Exception as errmsg:
            print(errmsg)
            raise CritError(messages.crit_error_no_file % program_output)

        if self.makelog: 
            if not (metadata.makelog_started and os.path.isfile(self.makelog)):
                raise CritError(messages.crit_error_no_makelog % self.makelog)
            with open(self.makelog, 'a') as f:
                f.write(out)

        if self.log: 
            if program_output != log:
                shutil.copy2(program_output, log)
                os.remove(program_output)
        else: 
            os.remove(program_output)


class SASDirective(ProgramDirective):    

    def __init__(self, 
                 lst = '', 
                 **kwargs):

        super(SASDirective, self).__init__(**kwargs)
        self.lst = lst  


class LyxDirective(ProgramDirective):    

    def __init__(self, 
                 doctype = '',
                 pdfout = metadata.settings['output_dir'],
                 **kwargs):

        super(LyxDirective, self).__init__(**kwargs)
        self.doctype = doctype
        self.pdfout  = pdfout
        self.get_pdfout()

    def get_pdfout(self):
        if self.doctype:
            self.pdfout = metadata.settings['temp_dir']

        self.pdfout = norm_path(self.pdfout)