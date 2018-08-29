# Modules
from __future__ import absolute_import, division, print_function, unicode_literals
from builtins import (bytes, str, open, super, range,
                      zip, round, input, int, pow, object)

import os 
os.chdir("/Users/zong/gslab_make/gslab_make_dev")

import run_program
import dir_mod
import create_links
import write_link_logs
import write_logs

# Clear directories
dir_mod.clear_dir(['../input', '../output', '../log'])

# Start make log
write_logs.start_makelog()

# Create links
links = create_links.create_links(['refactor_tests/links.txt'])
write_link_logs.write_link_logs(links)

# Run programs
run_program.run_python(program = 'refactor_tests/python.py', log = '../output/python.log')
run_program.run_r(program = 'refactor_tests/r.R', log = '../output/r.log')
run_program.run_stata(program = 'refactor_tests/stata.do', log = '../output/stata.log')
run_program.run_lyx(program = 'refactor_tests/lyx.lyx')
run_program.execute_command(command = 'ls', shell = True, log = '../output/command.log')

# Log outputs
write_logs.write_output_logs()

# End make log
write_logs.end_makelog()
