Specifying paths
================
The majority of the functions in :mod:`gslab_make` contain a ``paths`` argument that requires passing in a dictionary specifying default paths used for a variety of purposes. To fully use any function in the library, the dictionary *must* contain values for the following keys (i.e., default paths):

:config: Default path for ``config.yaml``, a *project configuration file* containing global variables for all users.
:config_user: Default path for ``config_user.yaml``, a *user configuration file* containing local user-specific variables.
:input_dir: Default path for sourcing (i.e., copying or making symbolic links to) *input files* located internal to the project directory.
:external_dir: Default path for sourcing (i.e., copying or making symbolic links to) *external files* located external to the project directory.
:output_dir: Default path to write and look for code outputs.
:makelog: Default path to write *make log*, a master log of activity.
:output_statslog: Default path to write *output statistics log*, a log containing file statistics for ``output_dir``.
:source_maplog: Default path to write *source mapping log*, a log that maps the original location for all sources in ``input_dir`` and ``external_dir``.
:source_statslog: Default path to write *source statistics log*, a log containing file statistics for all sources in ``input_dir`` and ``external_dir``.

.. Note:: 
   To suppress writing any specific log, set the value for that log to ``''``.

.. Warning::
   Many of the functions in :mod:`gslab_make` will write status messages to the make log. If you have specified a make log in your ``paths``, you must initialize the makelog via :py:func:`.start_makelog`. Otherwise, attempting to call a function that writes to the make log will raise an exception.

Example paths
-------------

The following default paths are recommended:

.. code-block:: python
    
    import os

    CONFIG_DIR = '..' # Adjust accordingly 

    PATHS = {
        'config'           : os.path.join(CONFIG_DIR, 'config.yaml'),
        'config_user'      : os.path.join(CONFIG_DIR, 'config_user.yaml'),
        'input_dir'        : 'input', 
        'external_dir'     : 'external',
        'output_dir'       : 'output',
        'makelog'          : 'log/make.log',         
        'output_statslog'  : 'log/output_stats.log', 
        'source_maplog'    : 'log/source_map.log',  
        'source_statslog'  : 'log/source_stats.log',
    }

Functions in :mod:`gslab_make` that require a ``paths`` argument will specify the exact default paths required in their documentation.


General logging functions
=========================

The :mod:`gslab_make` library provides functions to create a master log of activity (i.e., a *make log*) and to log information about output files. The logs are intended to facilitate the reproducibility of research.

.. Warning::
   You must initialize make logs via :py:func:`.start_makelog` as opposed to alternative methods (e.g., manually creating a make log file). Otherwise, any attempt to call a :mod:`gslab_make` function that writes to make log will raise an exception.

.. automodule:: gslab_make.write_logs
    :members:


Sourcing functions
==================

The :mod:`gslab_make` library provides functions to create symbolic links to source files. Doing so avoids potential duplication of source files and any associated confusion. In the case of modules dedicated to LyX/LaTeX documents, there are optional functions to copy source files instead of creating symbolic links so that users without :mod:`gslab_make` can still manually compile.

.. automodule:: gslab_make.move_sources
    :members:


Source logging functions
========================

The :mod:`gslab_make` library provides functions to log symbolic linking/copying activity and information about source files. The logs are intended to facilitate the reproducibility of research.

.. automodule:: gslab_make.write_source_logs
    :members:


Program functions
=================

The :mod:`gslab_make` library provides functions to run code scripts (i.e., *programs*) for certain applications. These program functions are implemented as Python wrappers around system commands.

.. Note:: 
   To use the program function for a specific application, please make sure that you have set up command line usage for the application.

Default settings
----------------
Unless specified otherwise, the program functions will assume the following default executables when executing your program. 
 
.. code-block:: python

    default_executables = {
        'posix': 
            {'lyx'       : 'lyx',
             'perl'      : 'perl',
             'python'    : 'python',
             'math'      : 'math',
             'matlab'    : 'matlab',
             'r'         : 'Rscript',
             'sas'       : 'sas', 
             'st'        : 'st',
             'stata'     : 'stata-mp'},
        'nt': 
            {'lyx'       : 'lyx',
             'perl'      : 'perl',
             'python'    : 'python',
             'matlab'    : 'matlab',
             'math'      : 'math',
             'r'         : 'Rscript',
             'sas'       : 'sas', 
             'st'        : 'st',
             'stata'     : '%STATAEXE%'}
 
To change the default executables, we recommend importing in a user configuration file using the :py:func:`.update_executables`. We do not recommend passing in an executable name into the ``executable`` argument of your program function as this will be global for any user.

The program functions will assume the following default options when executing system command.

.. code-block:: python 

    default_options = {
        'posix': 
            {'lyx'       : '-e pdf2',
             'perl'      : '',
             'python'    : '',
             'math'      : '-noprompt',
             'matlab'    : '-nosplash -nodesktop',
             'r'         : '--no-save',
             'st'        : '',
             'sas'       : '', 
             'stata'     : '-e'},
        'nt': 
            {'lyx'       : '-e pdf2',
             'perl'      : '',
             'python'    : '',
             'matlab'    : '-nosplash -minimize -wait',
             'math'      : '-noprompt',
             'r'         : '--no-save',
             'st'        : '',
             'sas'       : '-nosplash', 
             'stata'     : '/e'}
    }
    
To change the default options, you may pass your desired options into the ``options`` argument of your program function.

Supported applications
----------------------
.. automodule:: gslab_make.run_program
    :members:

Utility functions
=================

The :mod:`gslab_make` library provides general utility functions for build scripts. Functions to update executable names/path mappings and copy outputs are included.

.. automodule:: gslab_make.make_utility
    :members:

Directory functions
===================

The :mod:`gslab_make` library provides functions to make modifications to a directory. Functions to remove files and directories, clear directories, and zip/unzip files are included.

.. automodule:: gslab_make.modify_dir
    :members:

Repository functions
====================

The :mod:`gslab_make` library provides functions to check file sizes in a repository and modification status of files tracked by git. The checks are intended to facilitate proper committing activity.

.. automodule:: gslab_make.check_repo
    :members:

Filling functions
=================

The :mod:`gslab_make` library provides functions fill in tables and text in LyX/LaTeX documents.

.. automodule:: gslab_make.tablefill
    :members:
