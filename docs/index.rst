sphinx-exec-directive
=====================

``sphinx-exec-directive`` is a Sphinx extension which allows you to write code blocks in reStructuredText files, execute them during Sphinx compilation, and display the output directly within the generated documentation.

The default code language is Python, but there is some limited support for other languages right now.
Note that, for other languages, you will generally need to have the relevant executables in ``$PATH``.

This is based very strongly on `matplotlib's plot_directive extension <https://matplotlib.org/stable/api/sphinxext_plot_directive_api.html?highlight=plot%20directive#module-matplotlib.sphinxext.plot_directive>`_, but is used for running code instead of generating plots.

You are currently viewing the documentation for version |version| of ``sphinx-exec-directive``.

Contents
--------

.. toctree::
   :maxdepth: 3
   :glob:
   
   installation
   basic
   options
   language/index

* :ref:`genindex`
* :ref:`search`
