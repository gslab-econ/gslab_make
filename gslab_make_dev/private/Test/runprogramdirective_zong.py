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
        self.create_paths()

    def create_paths(self):    
        self.makelog   = os.path.abspath(self.makelog)
        self.log       = os.path.abspath(self.log) if log != '' else log
        
    def check_os(self):
        if (self.osname != 'posix') & (self.osname != 'nt'):
            raise CritError(messages.crit_error_unknown_system % self.osname)

    def run_command(self, command):   
        # Execute command
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

    def create_log(self, output)
        if self.log:
            with open(self.log, 'wb') as f:
                f.write(output)

        if self.makelog: 
            if not (metadata.makelog_started and os.path.isfile(self.makelog)):
                raise CritError(messages.crit_error_nomakelog % self.makelog)
            with open(self.makelog, 'wb') as f:
                f.write(log_text)

class ProgramDirective(Directive):

    def __init__(self, 
                 executable = '', 
                 option = '',
                 program,
                 args = '', 
                 **kwargs):

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

    def move_program_output(self, program_output, log = ''): 

    '''
    Certain programs create outputs that need to be moved to appropriate logging files
    '''
        try:
            with open(program_out, 'rb') as f:
                output = f.read()
        except Exception as errmsg:
            print(errmsg)
            raise CritError(messages.crit_error_no_file % program_out)

        if self.makelog: 
            if not (metadata.makelog_started and os.path.isfile(self.makelog)):
                raise CritError(messages.crit_error_nomakelog % self.makelog)
            with open(self.makelog, 'wb') as f:
                f.append(out)

        if log: 
            shutil.copy2(program_out, log)
        
        os.remove(program_out)

class SASDirective(ProgramDirective):    

    def __init__(self, 
                 lst = '', 
                 **kwargs):

        super(Directive, self).__init__(**kwargs)
        self.lst = lst  

class LyxDirective(ProgramDirective):    

    def __init__(self, 
                 handout = False, 
                 comments = False, 
                 pdfout = BLAH, 
                 **kwargs):

        super(Directive, self).__init__(**kwargs)
        self.handout  = handout
        self.comments = comments
        self.pdfout   = pdfout
        self.get_pdfout_dir()

    def get_pdf_out():
        if self.handout or self.comments:
            pdfout_dir = metadata.settings['temp_dir']
         else:
            pdfout_dir = metadata.settings['output_dir']