#! /usr/bin/env python

import os
import shutil
import subprocess

from exceptionclasses import CustomError, CritError, SyntaxError, LogicError
import messages as messages
import metadata as metadata

class Directive(object):

    def __init__(self, 
                 osname = os.name,
                 makelog = metadata.settings['makelog_file'], 
                 log = ''):

        self.osname   = osname
        self.makelog  = makelog
        self.log      = log  
        self.check_os()
        self.get_paths()

    def check_os(self):
        if (self.osname != 'posix') & (self.osname != 'nt'):
            raise CritError(messages.crit_error_unknown_system % self.osname)

    def get_paths(self):    
        self.makelog  = os.path.abspath(self.makelog)
        self.log      = os.path.abspath(self.log) if self.log != '' else self.log        

    def execute_command(self, command):   
        command = command.split()
        self.output = 'Executing: "' + ' '.join(command) + "'"
        print(self.output)
            
        try:   
             p = subprocess.Popen(command, stdout = subprocess.PIPE, stderr = subprocess.PIPE)
             out, err = p.communicate()
             print(err)
             self.output += '\n' + out + '\n' + err
        except Exception as errmsg:
             error_message = messages.crit_error_bad_command % ' '.join(command), '\n', str(errmsg)
             print(error_message)
             self.output += '\n' + error_message

    def write_log(self):
        if self.makelog: 
            if not (metadata.makelog_started and os.path.isfile(self.makelog)):
                raise CritError(messages.crit_error_nomakelog % self.makelog)
            with open(self.makelog, 'ab') as f:
                f.write(self.output)

        if self.log:
            with open(self.log, 'wb') as f:
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
        self.program      = os.path.abspath(self.program)
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
            program_output = os.path.abspath(program_output)
            with open(program_output, 'rb') as f:
                out = f.read()
        except Exception as errmsg:
            print(errmsg)
            raise CritError(messages.crit_error_no_file % program_output)

        if self.makelog: 
            if not (metadata.makelog_started and os.path.isfile(self.makelog)):
                raise CritError(messages.crit_error_nomakelog % self.makelog)
            with open(self.makelog, 'ab') as f:
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

    def get_pdfout():
        if not self.doctype:
            self.pdfout = metadata.settings['temp_dir']

        self.pdfout = os.path.abspath(self.pdfout)