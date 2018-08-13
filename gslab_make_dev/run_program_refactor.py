import os
import shutil
import fileinput

def run_stata(**kwargs):

    try:
        directive = ProgramDirective(**kwargs)

        # Get program output
        program_log = os.path.join(directive.program_path, directive.program_name + '.log')

        # Execute
        command = metadata.commands['stata'] % (directive.executable, directive.option, directive.program)
        directive.run_command(command)
        directive.move_program_output(program_log, directive.log)
		
    except:
        ERROR


def run_matlab(**kwargs)

    try:
        directive = ProgramDirective(**kwargs)
        
        # Get program output
        program_log = os.path.join(directive.program_path, directive.program_name + '.log')

        # Execute
        command = metadata.commands['matlab'] % (directive.executable, directive.program, directive.program_name + '.log', option)
        directive.run_command(command)
        directive.move_program_output(program_log, directive.log)
		
    except:
        ERROR


def run_perl(**kwargs):

    try:
        directive = ProgramDirective(**kwargs)
        
        # Execute
        command = metadata.commands['perl'] % (directive.executable, directive.option, directive.program, directive.args)
        directive.run_command(command)
    except:
        ERROR


def run_python(**kwargs):

    try:
        directive = ProgramDirective(**kwargs)

        # Execute
        command = metadata.commands['python'] % (directive.executable, directive.option, directive.program, directive.args)
        directive.run_command(command)
    except:
        ERROR


def run_mathematica(**kwargs):

    try:
        directive = ProgramDirective(**kwargs)

        # Execute
        command = metadata.commands['math'] % (directive.executable, directive.program, option)
        directive.run_command(command)
    except:
        ERROR


def run_stat_transer(**kwargs):

    try:
        directive = ProgramDirective(**kwargs)

        # Execute
        command = metadata.commands['st'] % (directive.executable, program)
        directive.run_command(command)
    except:
        ERROR


def run_lyx(**kwargs): # Check
    """
	Export a LyX file to PDF

    Example: 
	    To create PDF for 'draft.lyx', use command:
        `run_lyx(program = 'draft.lyx')`
    """

    try:
        directive = ProgramDirective(**kwargs)
            
        # Make handout/commented LyX file
        handout = directive.handout
        comments = directive.comments

		if handout:
		    program_name_suffix = '_handout'
		else if comments: 
		    program_name_suffix = '_comments'		
		
        if handout or comments:
            temp_program_name = directive.program_name + program_name_suffix
            temp_program_full = os.path.join(directive.program_path, temp_program_name + '.lyx') 
            
            program = program.replace(program_name, temp_program_name)
            program_name = temp_program_name
            
            beamer = False
            shutil.copy2(directive.program_full, temp_program_full)  # ITEM: Replace program_full appropriately!!!
            for line in fileinput.input(temp_program_full, inplace = True):
                if r'\textclass beamer' in line:
                    beamer = True
                elif handout and r'\options' in line and beamer:
                    line = line.rstrip('\n') + ', handout\n'
                elif comments and r'\begin_inset Note Note' in line:
                    line = line.replace('Note Note', 'Note Greyedout')
        
        # Execute
        command = metadata.commands['lyx'] % (directive.executable, directive.option, directive.program)
        directive.run_command(command)

        # Move PDF output
        pdf_name = os.path.join(directive.program_path, program_name + '.pdf')
        pdf_out = directive.pdf_out
		
        if os.path.abspath(pdf_name) != os.path.abspath(pdf_out):
            shutil.copy2(pdf_name, pdf_out)
            os.remove(pdf_name)
            
        # Remove handout/commented LyX file
        if handout or comments:
            os.remove(temp_program_full)

    except:
        ERROR


def run_r(**kwargs):

    try:
        directive = ProgramDirective(**kwargs)

		# Get program output
        program_log = os.path.join(directive.program_path, directive.program_name + '.Rout')

        # Execute
        command = metadata.commands['r'] % (directive.executable, directive.option, directive.program, directive.program_name + '.Rout')
        directive.run_command(command)
        directive.move_program_output(program_log, directive.log)
		
    except:
        ERROR


def run_sas(**kwargs):
    try:
        directive = ProgramDirective(**kwargs)

	    # Get program outputs
        program_log = os.path.join(directive.program_path, directive.program_name + '.log')
        program_lst = os.path.join(directive.program_path, directive.program_name + '.lst')
		
        # Execute
        command = metadata.commands['sas'] % (directive.executable, directive.option, directive.program)       
        directive.run_command(command)
        directive.move_program_output(default_log)
        directive.move_program_output(default_lst)
		
    except:
        ERROR


def run_command(command, **kwargs):
    """
	Run a shell command
	"""

    try:
	    directive = RunDirective(**kwargs)
		
		# Execute
		directive.execute_run(command)
	
    except:
        ERROR
