Installation
============

You can install from PyPI directly:

.. code-block:: bash

   pip install sphinx-exec-directive

or use the latest version of the repository (please raise an issue if the PyPI version is too old):

.. code-block:: bash

   git clone https://github.com/yongrenjie/sphinx-exec-directive
   cd sphinx-exec-directive
   pip install .


----

To enable the extension in a Sphinx project, place this in your Sphinx ``conf.py`` file.

.. warning::
   Note that this uses underscores, not hyphens. (This was probably a mistake, but I can't fix it now in a backward-compatible way.)

.. code-block:: python

   extensions = [
       sphinx_exec_directive,
       # other extensions...
   ]
