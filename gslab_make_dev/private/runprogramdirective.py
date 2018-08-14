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

        self.osname    = osname
        self.makelog   = makelog
        self.log       = log  
        self.get_paths()
		self.check_os()

    def get_paths(self):    
        self.makelog   = os.path.abspath(self.makelog)
        self.log       = os.path.abspath(self.log) if log != '' else log
        
    def check_os(self):
        if (self.osname != 'posix') & (self.osname != 'nt'):
            raise CritError(messages.crit_error_unknown_system % self.osname)

    def execute_command(self, command):   
        output = 'Executing: "' + ' '.join(command) + "'"
        print(output)
            
        try:   
             p = subprocess.Popen(command, stdout = subprocess.PIPE, stderr = subprocess.PIPE)
             out, err = p.communicate()
             print(err)
             output += '\n' + out + '\n' + err
        except Exception as errmsg:
             error_message = messages.crit_error_bad_command % ' '.join(command), '\n', str(errmsg)
             print(error_message)
             output += '\n' + error_message

        return(output)

    def write_log(self, output)
        if self.makelog: 
            if not (metadata.makelog_started and os.path.isfile(self.makelog)):
                raise CritError(messages.crit_error_nomakelog % self.makelog)
            with open(self.makelog, 'wb') as f:
                f.append(output)

        if self.log:
            with open(self.log, 'wb') as f:
                f.write(output)

class ProgramDirective(Directive):

    def __init__(self, 
                 application, 
                 executable = '', 
                 option = '',
                 program,
                 args = '', 
                 **kwargs):

        super(Directive, self).__init__(**kwargs)
        self.application = application
        self.executable  = executable
        self.option      = option
        self.program     = program
        self.args        = args      
        self.get_executable()
        self.get_option()
        self.parse_program()
        self.check_program()
		
    def get_executable(self):
        if not self.executable:
            self.executable = metadata.default_executables[self.osname][self.application]

	def get_option(self):
        if not self.option:
            self.option = metadata.default_options[self.osname][self.application]
			
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

    def move_program_output(self, output, log = ''): 
    '''
    Certain programs create outputs that need to be moved to appropriate logging files
    '''
        try:
            output = os.path.abspath(output)
            with open(output, 'rb') as f:
                output = f.read()
        except Exception as errmsg:
            print(errmsg)
            raise CritError(messages.crit_error_no_file % output)

        # TODO: DOUBLE-CHECK PATHS
       if self.makelog: 
            if not (metadata.makelog_started and os.path.isfile(self.makelog)):
                raise CritError(messages.crit_error_nomakelog % self.makelog)
            with open(self.makelog, 'wb') as f:
                f.append(out)

        if self.log: 
            if output != log:
                shutil.copy2(output, log)
    
		os.remove(output)

class SASDirective(ProgramDirective):    

    def __init__(self, 
                 lst = '', 
                 **kwargs):

        super(Directive, self).__init__(**kwargs)
        self.lst = lst  

class LyxDirective(ProgramDirective):    

    def __init__(self, 
                 doctype = '',
                 pdfout = metadata.settings['output_dir'],
                 **kwargs):

        super(Directive, self).__init__(**kwargs)
        self.doctype  = doctype
        self.pdfout  = pdfout
        self.get_pdfout()

    def get_pdfout():
        if not self.doctype:
            self.pdfout = metadata.settings['temp_dir']

        self.pdfout = os.path.abspath(self.pdfout)