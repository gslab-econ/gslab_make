# Modules
from __future__ import absolute_import, division, print_function
from builtins import (bytes, str, open, super, range,
                      zip, round, input, int, pow, object)

import os 
os.chdir("/Users/zong/gslab_make/gslab_make_dev")
os.chdir("C:\\Users\\zong\\gslab_make\\gslab_make_dev")

import run_program
import dir_mod
import make_link_logs
import make_links
import make_logs

# Clear directories
dir_mod.clear_dir(['../input', '../output', '../log'])

# Start make log
make_logs.start_makelog()

# Tests
# run_program.run_matlab(program = "_tests/matlab.m", log = "_tests/matlab.log")
# run_program.run_python(program = "_tests/python.py", log = "refactor_tests/python.log")
# run_program.run_r(program = "_tests/r.R", log = "refactor_tests/r.log")
# run_program.run_stata(program = "_tests/stata.do", log = "_tests/stata.log")

run_program.execute_command(command = "1+1", shell = True, log = "refactor_tests/command.log")

# End make log
make_logs.end_makelog()