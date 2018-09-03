#! /usr/bin/env python

# Import modules
from gslab_make_dev import run_program, dir_mod, create_links, write_link_logs, write_logs

# Clear directories
dir_mod.check_os()
dir_mod.clear_dir(['../input', '../output', '../temp', '../log'])

# Start make log
write_logs.set_option()
write_logs.start_makelog()

# Create links
links = create_links.create_links(['refactor_tests/links.txt'])
write_link_logs.write_link_logs(links)

# Run programs

# Log outputs
write_logs.write_output_logs()

# End make log
write_logs.end_makelog()

