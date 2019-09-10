#! /usr/bin/env python
from __future__ import absolute_import, division, print_function, unicode_literals
from future.utils import raise_from
from builtins import (bytes, str, open, super, range,
                      zip, round, input, int, pow, object)

import os
import re
import traceback
import shutil
import fileinput
import sys
import nbformat
from nbconvert.preprocessors import ExecutePreprocessor

from termcolor import colored
import colorama
colorama.init()

import gslab_make.private.messages as messages
import gslab_make.private.metadata as metadata
from gslab_make.private.exceptionclasses import CritError, ColoredError, ProgramError
from gslab_make.private.programdirective import Directive, ProgramDirective, SASDirective, LyXDirective
from gslab_make.private.utility import get_path, format_message, norm_path
from gslab_make.write_logs import write_to_makelog


def run_stata(paths, program, **kwargs):
    """ Run Stata script using system command.

    Parameters
    ----------
    paths : dict 
        Dictionary of paths. Dictionary should contain {
            'makelog' : str
                Path of makelog.
        }
    program : str
        Path of script to run.
    osname : str, optional
        Name of OS. Defaults to `os.name`.
    shell : bool, optional
        See: https://docs.python.org/2/library/subprocess.html#frequently-used-arguments.
        Defaults to `True`.
    log : str, optional
        Path of program log. Program log is only written if specified. 
    executable : str, optional
        Executable to use for system command. 
        Defaults to executable specified in metadata.
    option : str, optional
        Options for system command. Defaults to options specified in metadata.
    args : str, optional
        Not applicable.

    Returns
    -------
    None
    """

    try:
        makelog = get_path(paths, 'makelog')
        direct = ProgramDirective(application = 'stata', program = program, makelog = makelog, **kwargs)

        # Get program output
        program_name = direct.program.split(" ")[0]
        program_name = os.path.split(program_name)[-1]
        program_name = os.path.splitext(program_name)[0]
        program_log = os.path.join(os.getcwd(), program_name + '.log')
        
        # Sanitize program 
        if direct.osname == "posix":
            direct.program = re.escape(direct.program)

        # Execute
        command = metadata.commands[direct.osname]['stata'] % (direct.executable, direct.option, direct.program)
        exit_code, stderr = direct.execute_command(command)
        if exit_code != 0:
            error_message = 'Stata program executed with errors. Traceback can be found below.'
            error_message = format_message(error_message)
            raise_from(ProgramError(error_message, stderr), None)
        output = direct.move_program_output(program_log, direct.log)
        check_stata_output(output)
    except ProgramError:
        raise
    except:
        error_message = 'Error with `run_stata`. Traceback can be found below.' 
        error_message = format_message(error_message) 
        write_to_makelog(paths, error_message + '\n\n' + traceback.format_exc())
        raise_from(ColoredError(error_message, traceback.format_exc()), None)
    
    
def check_stata_output(output):
    regex = "end of do-file[\s]*r\([0-9]*\);"
    if re.search(regex, output):
        error_message = 'Stata program executed with errors.'
        error_message = format_message(error_message)
        raise_from(ProgramError(error_message, 'See makelog for more detail.'), None)


def run_matlab(paths, program, **kwargs):
    """ Run Matlab script using system command.

    Parameters
    ----------
    paths : dict 
        Dictionary of paths. Dictionary should contain {
            'makelog' : str
                Path of makelog.
        }
    program : str
        Path of script to run.
    osname : str, optional
        Name of OS. Defaults to `os.name`.
    shell : bool, optional
        See: https://docs.python.org/2/library/subprocess.html#frequently-used-arguments.
        Defaults to `True`.
    log : str, optional
        Path of program log. Program log is only written if specified. 
    executable : str, optional
        Executable to use for system command. 
        Defaults to executable specified in metadata.
    option : str, optional
        Options for system command. Defaults to options specified in metadata.
    args : str, optional
        Not applicable.

    Returns
    -------
    None
    """

    try:
        makelog = get_path(paths, 'makelog')
        direct = ProgramDirective(application = 'matlab', program = program, makelog = makelog, **kwargs)
        
        # Get program output
        program_log = os.path.join(os.getcwd(), direct.program_name + '.log')

        # Execute
        command = metadata.commands[direct.osname][direct.application] % (direct.executable, direct.option, direct.program, direct.program_name + '.log')
        exit_code, stderr = direct.execute_command(command)   
        if exit_code != 0:
            error_message = 'Matlab program executed with errors. Traceback can be found below.'
            error_message = format_message(error_message)
            raise_from(ProgramError(error_message, stderr), None)
        direct.move_program_output(program_log, direct.log)   
    except ProgramError:
        raise
    except:
        error_message = 'Error with `run_matlab`. Traceback can be found below.' 
        error_message = format_message(error_message) 
        write_to_makelog(paths, error_message + '\n\n' + traceback.format_exc())
        raise_from(ColoredError(error_message, traceback.format_exc()), None)
        

def run_perl(paths, program, **kwargs):
    """ Run Perl script using system command.

    Parameters
    ----------
    paths : dict 
        Dictionary of paths. Dictionary should contain {
            'makelog' : str
                Path of makelog.
        }
    program : str
        Path of script to run.
    osname : str, optional
        Name of OS. Defaults to `os.name`.
    shell : bool, optional
        See: https://docs.python.org/2/library/subprocess.html#frequently-used-arguments.
        Defaults to `True`.
    log : str, optional
        Path of program log. Program log is only written if specified. 
    executable : str, optional
        Executable to use for system command. 
        Defaults to executable specified in metadata.
    option : str, optional
        Options for system command. Defaults to options specified in metadata.
    args : str, optional
        Arguments for system command. Defaults to no arguments.

    Returns
    -------
    None
    """

    try:
        makelog = get_path(paths, 'makelog')
        direct = ProgramDirective(application = 'perl', program = program, makelog = makelog, **kwargs)
        
        # Execute
        command = metadata.commands[direct.osname][direct.application] % (direct.executable, direct.option, direct.program, direct.args)
        exit_code, stderr = direct.execute_command(command)
        direct.write_log()
        if exit_code != 0:
            error_message = 'Perl program executed with errors. Traceback can be found below.'
            error_message = format_message(error_message)
            raise_from(ProgramError(error_message, stderr), None)
    except ProgramError:
        raise
    except:
        error_message = 'Error with `run_perl`. Traceback can be found below.' 
        error_message = format_message(error_message) 
        write_to_makelog(paths, error_message + '\n\n' + traceback.format_exc())
        raise_from(ColoredError(error_message, traceback.format_exc()), None)


def run_python(paths, program, **kwargs):
    """ Run Python script using system command.

    Parameters
    ----------
    paths : dict 
        Dictionary of paths. Dictionary should contain {
            'makelog' : str
                Path of makelog.
        }
    program : str
        Path of script to run.
    osname : str, optional
        Name of OS. Defaults to `os.name`.
    shell : bool, optional
        See: https://docs.python.org/2/library/subprocess.html#frequently-used-arguments.
        Defaults to `True`.
    log : str, optional
        Path of program log. Program log is only written if specified. 
    executable : str, optional
        Executable to use for system command. 
        Defaults to executable specified in metadata.
    option : str, optional
        Options for system command. Defaults to options specified in metadata.
    args : str, optional
        Arguments for system command. Defaults to no arguments.

    Returns
    -------
    None
    """

    try:
        makelog = get_path(paths, 'makelog')
        direct = ProgramDirective(application = 'python', program = program, makelog = makelog, **kwargs)

        # Execute
        command = metadata.commands[direct.osname][direct.application] % (direct.executable, direct.option, direct.program, direct.args)
        exit_code, stderr = direct.execute_command(command)
        direct.write_log() 
        if exit_code != 0:
            error_message = 'Python program executed with errors. Traceback can be found below.'
            error_message = format_message(error_message)
            raise_from(ProgramError(error_message, stderr), None)
    except ProgramError:
        raise
    except:
        error_message = 'Error with `run_python`. Traceback can be found below.' 
        error_message = format_message(error_message) 
        write_to_makelog(paths, error_message + '\n\n' + traceback.format_exc())
        raise_from(ColoredError(error_message, traceback.format_exc()), None)
        

def run_jupyter(paths, program, timeout = None, kernel_name = ''):
    """ Run Jupyter notebook using system command.

    Parameters
    ----------
    paths : dict 
        Dictionary of paths. Dictionary should contain {
            'makelog' : str
                Path of makelog.
        }
    program : str
        Path of script to run.
    timeout : int
        Time to wait (in seconds) for execution outputs before raising exception.
        Defaults to no timeout.
    kernel_name : str
        Name of kernel to use for execution.
        Defaults to kernel specified in notebook.
    Returns
    -------
    None
    """

    try:
        makelog = get_path(paths, 'makelog')
        program = norm_path(program)

        with open(program) as f:
            message = 'Processing notebook: `%s`' % program
            write_to_makelog(paths, message)    
            print(colored(message, 'cyan'))
            
            if not kernel_name:
                kernel_name = 'python%s' % sys.version_info[0]

            ep = ExecutePreprocessor(timeout = timeout, kernel_name = kernel_name)
            nb = nbformat.read(f, as_version = 4)       
            ep.preprocess(nb, {'metadata': {'path': '.'}})
        with open(program, 'wt') as f:
            nbformat.write(nb, f)
    except:
        error_message = 'Error with `run_jupyter`. Traceback can be found below.' 
        error_message = format_message(error_message) 
        write_to_makelog(paths, error_message + '\n\n' + traceback.format_exc())
        raise_from(ColoredError(error_message, traceback.format_exc()), None)


def run_mathematica(paths, program, **kwargs):
    """ Run Mathematica script using system command.

    Parameters
    ----------
    paths : dict 
        Dictionary of paths. Dictionary should contain {
            'makelog' : str
                Path of makelog.
        }
    program : str
        Path of script to run.
    osname : str, optional
        Name of OS. Defaults to `os.name`.
    shell : bool, optional
        See: https://docs.python.org/2/library/subprocess.html#frequently-used-arguments.
        Defaults to `True`.
    log : str, optional
        Path of program log. Program log is only written if specified. 
    executable : str, optional
        Executable to use for system command. 
        Defaults to executable specified in metadata.
    option : str, optional
        Options for system command. Defaults to options specified in metadata.
    args : str, optional
        Not applicable.
        
    Returns
    -------
    None
    """
    
    try:
        makelog = get_path(paths, 'makelog')
        direct = ProgramDirective(application = 'math', program = program, makelog = makelog, **kwargs)

        # Execute
        command = metadata.commands[direct.osname][direct.application] % (direct.executable, direct.program, direct.option)
        exit_code, stderr = direct.execute_command(command)
        direct.write_log()
        if exit_code != 0:
            error_message = 'Mathematica program executed with errors. Traceback can be found below.'
            error_message = format_message(error_message)
            raise_from(ProgramError(error_message, stderr), None)
    except ProgramError:
        raise
    except:
        error_message = 'Error with `run_mathematica`. Traceback can be found below.' 
        error_message = format_message(error_message) 
        write_to_makelog(paths, error_message + '\n\n' + traceback.format_exc())
        raise_from(ColoredError(error_message, traceback.format_exc()), None)
        

def run_stat_transfer(paths, program, **kwargs):
    """ Run StatTransfer script using system command.

    Parameters
    ----------
    paths : dict 
        Dictionary of paths. Dictionary should contain {
            'makelog' : str
                Path of makelog.
        }
    program : str
        Path of script to run.
    osname : str, optional
        Name of OS. Defaults to `os.name`.
    shell : bool, optional
        See: https://docs.python.org/2/library/subprocess.html#frequently-used-arguments.
        Defaults to `True`.
    log : str, optional
        Path of program log. Program log is only written if specified. 
    executable : str, optional
        Executable to use for system command. 
        Defaults to executable specified in metadata.
    option : str, optional
        Options for system command. Defaults to options specified in metadata.
    args : str, optional
        Not applicable.

    Returns
    -------
    None
    """

    try:
        makelog = get_path(paths, 'makelog')
        direct = ProgramDirective(application = 'st', program = program, makelog = makelog, **kwargs)

        # Execute
        command = metadata.commands[direct.osname][direct.application] % (direct.executable, direct.program)
        exit_code, stderr = direct.execute_command(command)
        direct.write_log()
        if exit_code != 0:
            error_message = 'StatTransfer program executed with errors. Traceback can be found below.'
            error_message = format_message(error_message)
            raise_from(ProgramError(error_message, stderr), None)
    except ProgramError:
        raise
    except:
        error_message = 'Error with `run_stat_transfer`. Traceback can be found below.' 
        error_message = format_message(error_message) 
        write_to_makelog(paths, error_message + '\n\n' + traceback.format_exc())
        raise_from(ColoredError(error_message, traceback.format_exc()), None)
        

def run_lyx(paths, program, **kwargs): 
    """ Run LyX script using system command.

    Parameters
    ----------
    paths : dict 
        Dictionary of paths. Dictionary should contain {
            'makelog' : str
                Path of makelog.
            'pdf_dir' : str
                Directory to write PDFs.
        }
    program : str
        Path of script to run.
    osname : str, optional
        Name of OS. Defaults to `os.name`.
    shell : bool, optional
        See: https://docs.python.org/2/library/subprocess.html#frequently-used-arguments.
        Defaults to `True`.
    log : str, optional
        Path of program log. Program log is only written if specified. 
    executable : str, optional
        Executable to use for system command. 
        Defaults to executable specified in metadata.
    option : str, optional
        Options for system command. Defaults to options specified in metadata.
    args : str, optional
        Not applicable.
    doctype : str, optional
       Type of Lyx document. Takes either `handout` and `comments`. 
       Defaults to no special document type.
        
    Returns
    -------
    None
    """

    try:
        makelog = get_path(paths, 'makelog')
        pdf_dir = get_path(paths, 'pdf_dir')
        direct = LyXDirective(pdf_dir = pdf_dir, application = 'lyx', program = program, makelog = makelog, **kwargs)
            
        # Make handout/commented LyX file        
        if direct.doctype:
            temp_name = os.path.join(direct.program_name + '_' + direct.doctype)
            temp_program = os.path.join(direct.program_dir, temp_name + '.lyx') 
            
            beamer = False
            shutil.copy2(direct.program, temp_program) 

            # TODO: DOUBLE-CHECK
            for line in fileinput.input(temp_program, inplace = True):
                if r'\textclass beamer' in line:
                    beamer = True          
                if direct.doctype == 'handout' and r'\options' in line and beamer:
                    line = line.rstrip('\n') + ', handout\n'
                elif direct.doctype == 'comments' and r'\begin_inset Note Note' in line:
                    line = line.replace('Note Note', 'Note Greyedout')
                print(line)
        else:
            temp_name = direct.program_name
            temp_program = direct.program

        # Execute
        command = metadata.commands[direct.osname][direct.application] % (direct.executable, direct.option, temp_program)
        exit_code, stderr = direct.execute_command(command)
        direct.write_log()
        if exit_code != 0:
            error_message = 'LyX program executed with errors. Traceback can be found below.'
            error_message = format_message(error_message)
            raise_from(ProgramError(error_message, stderr), None)

        # Move PDF output
        temp_pdf = os.path.join(direct.program_dir, temp_name + '.pdf')
        output_pdf = os.path.join(direct.pdf_dir, direct.program_name + '.pdf')

        if temp_pdf != output_pdf:
            shutil.copy2(temp_pdf, output_pdf)
            os.remove(temp_pdf)
            
        # Remove handout/commented LyX file
        if direct.doctype:
            os.remove(temp_program)
    except ProgramError:
        raise
    except:
        error_message = 'Error with `run_lyx`. Traceback can be found below.' 
        error_message = format_message(error_message) 
        write_to_makelog(paths, error_message + '\n\n' + traceback.format_exc())
        raise_from(ColoredError(error_message, traceback.format_exc()), None)
        

def run_r(paths, program, **kwargs):
    """ Run R script using system command.

    Parameters
    ----------
    paths : dict 
        Dictionary of paths. Dictionary should contain {
            'makelog' : str
                Path of makelog.
        }
    program : str
        Path of script to run.
    osname : str, optional
        Name of OS. Defaults to `os.name`.
    shell : bool, optional
        See: https://docs.python.org/2/library/subprocess.html#frequently-used-arguments.
        Defaults to `True`.
    log : str, optional
        Path of program log. Program log is only written if specified. 
    executable : str, optional
        Executable to use for system command. 
        Defaults to executable specified in metadata.
    option : str, optional
        Options for system command. Defaults to options specified in metadata.
    args : str, optional
        Not applicable.

    Returns
    -------
    None
    """
    
    try:
        makelog = get_path(paths, 'makelog')
        direct = ProgramDirective(application = 'r', program = program, makelog = makelog, **kwargs)

        # Execute
        command = metadata.commands[direct.osname][direct.application] % (direct.executable, direct.option, direct.program)
        exit_code, stderr = direct.execute_command(command)
        direct.write_log()      
        if exit_code != 0:
            error_message = 'R program executed with errors. Traceback can be found below.'
            error_message = format_message(error_message)
            raise_from(ProgramError(error_message, stderr), None)
    except ProgramError:
        raise
    except:
        error_message = 'Error with `run_r`. Traceback can be found below.' 
        error_message = format_message(error_message) 
        write_to_makelog(paths, error_message + '\n\n' + traceback.format_exc())
        raise_from(ColoredError(error_message, traceback.format_exc()), None)
        

def run_sas(paths, program, **kwargs):
    """ Run SAS script using system command.

    Parameters
    ----------
    paths : dict 
        Dictionary of paths. Dictionary should contain {
            'makelog' : str
                Path of makelog.
        }
    program : str
        Path of script to run.
    osname : str, optional
        Name of OS. Defaults to `os.name`.
    shell : bool, optional
        See: https://docs.python.org/2/library/subprocess.html#frequently-used-arguments.
        Defaults to `True`.
    log : str, optional
        Path of program log. Program log is only written if specified. 
    executable : str, optional
        Executable to use for system command. 
        Defaults to executable specified in metadata.
    option : str, optional
        Options for system command. Defaults to options specified in metadata.
    args : str, optional
        Not applicable.
    lst : str, optional
        Path of program lst. Program lst is only written if specified. 
        
    Returns
    -------
    None
    """

    try:
        makelog = get_path(paths, 'makelog')
        direct = SASDirective(application = 'sas', program = program, makelog = makelog, **kwargs)

        # Get program outputs
        program_log = os.path.join(os.getcwd(), direct.program_name + '.log')
        program_lst = os.path.join(os.getcwd(), direct.program_name + '.lst')
        
        # Execute
        command = metadata.commands[direct.osname][direct.application] % (direct.executable, direct.option, direct.program)       
        exit_code, stderr = direct.execute_command(command)
        if exit_code != 0:
            error_message = 'SAS program executed with errors. Traceback can be found below.'
            error_message = format_message(error_message)
            raise_from(ProgramError(error_message, stderr), None)
        direct.move_program_output(program_log)
        direct.move_program_output(program_lst)        
    except ProgramError:
        raise
    except:
        error_message = 'Error with `run_sas`. Traceback can be found below.' 
        error_message = format_message(error_message) 
        write_to_makelog(paths, error_message + '\n\n' + traceback.format_exc())
        raise_from(ColoredError(error_message, traceback.format_exc()), None)
        

def execute_command(paths, command, **kwargs):
    """ Run system command.

    Parameters
    ----------
    paths : dict 
        Dictionary of paths. Dictionary should contain {
            'makelog' : str
                Path of makelog.
        }
    command : str
        system command to run.
    osname : str, optional
        Name of OS. Defaults to `os.name`.
    shell : bool, optional
        See: https://docs.python.org/2/library/subprocess.html#frequently-used-arguments.
        Defaults to `True`.
    log : str, optional
        Path of system command log. system command log is only written if specified. 
        
    Returns
    -------
    None
    """
    
    try:
        makelog = get_path(paths, 'makelog')
        direct = Directive(makelog = makelog, **kwargs)

        # Execute
        exit_code, stderr = direct.execute_command(command)
        direct.write_log()   
        if exit_code != 0:
            error_message = 'Command executed with errors. Traceback can be found below.'
            error_message = format_message(error_message)
            raise_from(ProgramError(error_message, stderr), None)
    except ProgramError:
        raise
    except:
        error_message = 'Error with `execute_command`. Traceback can be found below.' 
        error_message = format_message(error_message) 
        write_to_makelog(paths, error_message + '\n\n' + traceback.format_exc())
        raise_from(ColoredError(error_message, traceback.format_exc()), None)


def run_module(root, module, build_script = 'make.py'):
    """ Run module. 
    
    Parameters
    ----------
    root : str 
        Directory of root.
    module: str
        Name of module.
    build_script : str
        Name of build script.

    Returns
    -------
    None
    """

    try:
        module_dir = os.path.join(root, module)
        os.chdir(module_dir)

        build_script = norm_path(build_script)
        if not os.path.isfile(build_script):
            raise CritError(messages.crit_error_no_file % build_script)  

        message = 'Running module `%s`' % module
        message = format_message(message)
        message = colored(message, attrs = ['bold'])
        print('\n' + message)  

        status = os.system('python %s' % build_script)
        if status != 0:
            raise ProgramError()
    except ProgramError:
        sys.exit()
    except:
        error_message = 'Error with `run_module`. Traceback can be found below.' 
        error_message = format_message(error_message) 
        raise_from(ColoredError(error_message, traceback.format_exc()), None)