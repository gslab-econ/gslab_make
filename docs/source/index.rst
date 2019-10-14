*************
Documentation
*************
.. contents:: Table of Contents

Paths argument
==============
The majority of the functions in :mod:`gslab_make` contain a ``paths`` argument that requires passing in a dictionary specifying default paths used for writing and logging purposes. The dictionary *must* contain values for the following keys (i.e., default paths):

:config: Default path for `config.yaml` file.
:config_user: Default path for `config_user.yaml` file. 
:input_dir: Default path for writing symbolic links/copies to sources internal to the repository. 
:external_dir: Default path for writing symbolic links/copies to sources external to the repository. 
:output_dir: Default path for finding outputs for logging.
:makelog: Default path for writing make log.
:output_statslog: Default path for writing log containing output statistics.
:source_maplog: Default path for writing log containing source mappings.
:source_statslog: Default path for writing log containing source statistics.

.. Note:: 
   To suppress writing any specific log, set the key for that log to ``''``.

**Example**

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
        'output_local_dir' : 'output_local',
        'makelog'          : 'log/make.log',         
        'output_statslog'  : 'log/output_stats.log', 
        'source_maplog'    : 'log/source_map.log',  
        'source_statslog'  : 'log/source_stats.log',
    }

Functions in :mod:`gslab_make` that require a ``paths`` argument will specify the specific default paths required in their documentation.

Repository functions
====================

The following functions are used to check file size and modification status of files tracked by git. The logs are intended to facilitate proper committing activity.

.. automodule:: gslab_make.check_repo
    :members:

Program functions
=================

.. automodule:: gslab_make.run_program
    :members:

Utility functions
=================

.. automodule:: gslab_make.make_utility
    :members:

Directory functions
===================

.. automodule:: gslab_make.modify_dir
    :members:

Linking/copying functions
=========================

.. automodule:: gslab_make.move_sources
    :members:

Tablefill
=========

.. automodule:: gslab_make.tablefill
    :members:

Logging functions
=================

.. automodule:: gslab_make.write_logs
    :members:

Source logging functions
========================


.. automodule:: gslab_make.write_source_logs
    :members:

