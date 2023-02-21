Shell
=====

All shell scripts are run with ``sh``.

Note that in general, ``sh`` will not necessarily have the same behaviour as the shell which you use in your terminal (e.g. ``bash`` or ``zsh``): see ``man sh``, or `this Stack Overflow link <https://stackoverflow.com/questions/5725296>`_ for more details.
In particular, configuration files are not sourced.

However, you *will* have access to environment variables, notably including ``$PATH``.
This is because the subprocess which runs the code inherits environment variables from the calling process (i.e. Sphinx).

.. code-block:: rst
   :caption: rst

   .. exec::
      :process: shell
      
      echo "Hello, world; from sh."
      which ls
      seq 1 5
      alias

|hr|

.. exec::
   :process: shell
  
   echo "Hello, world; from sh."
   which ls
   seq 1 5
   alias
