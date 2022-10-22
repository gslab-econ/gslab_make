Sourcing functions
==================

The :mod:`gslab_make` library provides functions to create symbolic links to source files. Doing so avoids potential duplication of source files and any associated confusion. In the case of modules dedicated to LyX/LaTeX documents, there are optional functions to copy source files instead of creating symbolic links so that users without :mod:`gslab_make` can still manually compile.

.. automodule:: gslab_make.move_sources
    :members:
    :noindex:

.. toctree::
  :glob:
  :hidden:

  api/move_sources/*