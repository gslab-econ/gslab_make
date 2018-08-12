#! /usr/bin/env python

import os
import re
import shutil
import subprocess

from exceptionclasses import CustomError, CritError, SyntaxError, LogicError
import messages as messages
import metadata as metadata
import utility as utility

class Directive(object):

    def __init__(self, 
                 osname = os.name,
                 changedir = False, 
                 makelog = metadata.settings['makelog_file'], 
                 log = ''):

        self.osname    = osname
        self.changedir = changedir 
        self.makelog   = makelog
        self.log       = log  
        self.create_paths()

    def create_paths(self):    
        self.makelog   = os.path.abspath(self.makelog)
        self.log       = os.path.abspath(self.log) if log != '' else log
        
    def check_os(self):
        if (self.osname != 'posix') & (self.osname != 'nt'):
            raise CritError(messages.crit_error_unknown_system % self.osname)

    def execute_run(self, command):
        print '\n'

        # Change directory if specified
        current_dir = os.getcwd()
        
        if self.changedir:
            os.chdir(self.program_path)
        
        # Execute command
        try:
            output = "Executing" + command
            print(output)

            subprocess.check_call(command, shell = True, stdout = TEMPFILE, stderr = TEMPFILE)

            except Exception as errmsg:
            # If fails then print errors to LOGFILE
                TEMPFILE.close()
                LOGFILE.write(open(tempname, 'rU').read())
                print messages.crit_error_bad_command % command, '\n', str(errmsg)
                print >> LOGFILE, messages.crit_error_bad_command % command, '\n', str(errmsg)
                LOGFILE.close()

        # Create log
        if self.log:
            with open(self.log, 'wb') as f:
                f.write(BLAH)

        if self.makelog: 
            if not (metadata.makelog_started and os.path.isfile(self.makelog)):
                raise CritError(messages.crit_error_nomakelog % self.makelog)
            with open(self.makelog, 'wb') as f:
                f.write(BLAH)

        # Change directory back
        if self.changedir:
            os.chdir(current_dir)

class ProgramDirective(Directive):

    def __init__(self, 
                 executable = '', 
                 option = '',
                 program,
                 args = '', 
                 **kwargs)

        super(Directive, self).__init__(**kwargs)
        self.executable = executable
        self.option     = option
        self.program    = program
        self.args       = args       
        self.parse_program()

    def parse_program(self):
        self.program_path = os.path.dirname(program)
        self.program_base = os.path.basename(program)
        self.program_name, self.program_ext = os.path.splitext(program_base)

        if self.program_path == '':
            self.program_path = './'

    def check_program(self, application):
        if not os.path.isfile(self.program):
            raise CritError(messages.crit_error_no_file % self.program)
        if self.program_ext != metadata.extensions[application]:
            raise CritError(messages.crit_error_extension % self.program)