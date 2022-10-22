General logging functions
=========================

The :mod:`gslab_make` library provides functions to create a master log of activity (i.e., a *make log*) and to log information about output files. The logs are intended to facilitate the reproducibility of research.

.. Warning::
   You must initialize make logs via :py:func:`.start_makelog` as opposed to alternative methods (e.g., manually creating a make log file). Otherwise, any attempt to call a :mod:`gslab_make` function that writes to make log will raise an exception.

.. automodule:: gslab_make.write_logs
    :members:
    :noindex:

.. toctree::
  :glob:
  :hidden:

  api/write_logs/*

