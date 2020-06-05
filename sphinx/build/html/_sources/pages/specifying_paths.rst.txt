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