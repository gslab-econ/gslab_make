# Modules
from __future__ import absolute_import, division, print_function, unicode_literals
from builtins import (bytes, str, open, super, range,
                      zip, round, input, int, pow, object)

import os 
os.chdir("/Users/zong/gslab_make/gslab_make_dev")

import run_program
import dir_mod
import make_link_logs
import make_links
import make_logs

# Clear directories
dir_mod.clear_dir(['../input', '../output', '../log'])

# Start make log
make_logs.start_makelog()

# Create links
links = make_links.make_links(['refactor_tests/links.txt'])
make_link_logs.make_link_logs(links)

# Run programs
run_program.run_python(program = 'refactor_tests/python.py', log = '../output/python.log')
run_program.run_r(program = 'refactor_tests/r.R', log = '../output/r.log')
run_program.run_stata(program = 'refactor_tests/stata.do', log = '../output/stata.log')

run_program.execute_command(command = 'ls', shell = True, log = '../output/command.log')

# Log outputs
make_logs.make_output_logs()

# End make log
make_logs.end_makelog()
