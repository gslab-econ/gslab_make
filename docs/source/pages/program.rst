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
             'stata'     : 'StataMP-64'}
 
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
    :noindex:

.. toctree::
  :glob:
  :hidden:

  api/run_program/*