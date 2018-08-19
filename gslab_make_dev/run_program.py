import os
import shutil
import fileinput

import private.metadata as metadata
import private.messages as messages
from private.exceptionclasses import SyntaxError
from private.runprogramdirective import (Directive, 
                                         ProgramDirective, 
                                         SASDirective, 
                                         LyxDirective)

def run_stata(**kwargs):

    try:
        directive = ProgramDirective(application = 'stata', **kwargs)

        # Get program output
        program_log = os.path.join(os.getcwd(), directive.program_name + '.log')

        # Execute
        command = metadata.commands[directive.osname]['stata'] % (directive.executable, directive.option, directive.program)
        directive.execute_command(command)
        directive.write_log()
        directive.move_program_output(program_log, directive.log)       
    except Exception as e:
        print(e)


def run_matlab(**kwargs):

    try:
        directive = ProgramDirective(application = 'matlab', **kwargs)
        
        # Get program output
        program_log = os.path.join(os.getcwd(), directive.program_name + '.log')

        # Execute
        command = metadata.commands[directive.osname][directive.application] % (directive.executable, directive.option, directive.program, directive.program_name + '.log')
        directive.execute_command(command)    
        directive.move_program_output(program_log, directive.log)       
    except Exception as e:
        print(e)


def run_perl(**kwargs):

    try:
        directive = ProgramDirective(application = 'perl', **kwargs)
        
        # Execute
        command = metadata.commands[directive.osname][directive.application] % (directive.executable, directive.option, directive.program, directive.args)
        directive.execute_command(command)
        directive.write_log()
    except Exception as e:
        print(e)


def run_python(**kwargs):

    try:
        directive = ProgramDirective(application = 'python', **kwargs)

        # Execute
        command = metadata.commands[directive.osname][directive.application] % (directive.executable, directive.option, directive.program, directive.args)
        directive.execute_command(command)
        directive.write_log()
    except Exception as e:
        print(e)


def run_mathematica(**kwargs):

    try:
        directive = ProgramDirective(application = 'math', **kwargs)

        # Execute
        command = metadata.commands[directive.osname][directive.application] % (directive.executable, directive.program, directive.option)
        directive.execute_command(command)
        directive.write_log()
    except Exception as e:
        print(e)


def run_stat_transfer(**kwargs):

    try:
        directive = ProgramDirective(application = 'st', **kwargs)

        # Execute
        command = metadata.commands[directive.osname][directive.application] % (directive.executable, directive.program)
        directive.execute_command(command)
        directive.write_log()
    except Exception as e:
        print(e)


def run_lyx(**kwargs): # Check

    try:
        directive = LyxDirective(application = 'lyx', **kwargs)
            
        # Make handout/commented LyX file        
        if not directive.doctype:
            temp_name = os.path.join(directive.program_name + '_' + directive.doctype)
            temp_program = os.path.join(directive.program_path, temp_name + '.lyx') 
            
            beamer = False
            shutil.copy2(directive.program, temp_program) 
            for line in fileinput.input(temp_program, inplace = True):
                if r'\textclass beamer' in line:
                    beamer = True
                elif directive.doctype == 'handout' and r'\options' in line and beamer:
                    line = line.rstrip('\n') + ', handout\n'
                elif directive.doctype == 'comments' and r'\begin_inset Note Note' in line:
                    line = line.replace('Note Note', 'Note Greyedout')
        else:
             temp_name = directive.program_name
             temp_program = directive.program

        # Execute
        command = metadata.commands[directive.osname][directive.application] % (directive.executable, directive.option, temp_program)
        directive.execute_command(command)
        directive.write_log()

        # Move PDF output
        temp_pdf = os.path.join(directive.program_path, temp_name + '.pdf')
        
        if temp_pdf != directive.pdf_out:
            shutil.copy2(temp_pdf, directive.pdf_out)
            os.remove(temp_pdf)
            
        # Remove handout/commented LyX file
        if not directive.doctype:
            os.remove(temp_program)
    except Exception as e:
        print(e)


def run_r(**kwargs):

    try:
        directive = ProgramDirective(application = 'r', **kwargs)

        # Execute
        command = metadata.commands[directive.osname][directive.application] % (directive.executable, directive.option, directive.program)
        directive.execute_command(command)
        directive.write_log()      
    except Exception as e:
        print(e)


def run_sas(**kwargs):
    
    try:
        directive = ProgramDirective(application = 'sas', **kwargs)

        # Get program outputs
        program_log = os.path.join(os.getcwd(), directive.program_name + '.log')
        program_lst = os.path.join(os.getcwd(), directive.program_name + '.lst')
        
        # Execute
        command = metadata.commands[directive.osname][directive.application] % (directive.executable, directive.option, directive.program)       
        directive.execute_command(command)
        directive.move_program_output(program_log)
        directive.move_program_output(program_lst)        
    except Exception as e:
        print(e)


def execute_command(command, **kwargs):

    try:
        directive = Directive(**kwargs)

        # Execute
        directive.execute_command(command)
        directive.write_log()   
    except Exception as e:
        print(e)
