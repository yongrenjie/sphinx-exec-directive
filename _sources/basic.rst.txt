Basic usage: Python
===================

.. note::
   All RST inputs in this documentation are denoted by the ``rst_usage`` caption above the code block. This is to differentiate them from the code blocks which are generated as a result of using this plugin.
   
   Additionally, the RST inputs are always separated from the two output blocks by a horizontal line.

The simplest example is, naturally, a hello world.
Placing these lines in your RST file will generate two literal blocks, one with the input source code, and one with the captured standard output.
It looks pretty basic, but it does the job.
Here it is:

.. code-block:: rst
   :caption: rst

   .. exec::
      
      print("Hello, world.")

|hr|

.. exec::
  
   print("Hello, world.")


Note that objects **must** be printed to stdout, or they will not be displayed.
This behaviour therefore differs slightly from the functionality in a Jupyter notebook (where the last line is evaluated and the result displayed automatically), or the interactive Python console.

If nothing is printed to stdout (or only empty space is) then the output literal block will be omitted.
For example, the following generates only one code block with the input code, and no stdout block.

.. code-block:: rst
   :caption: rst

   .. exec::
      
      s = "Hello, world."
      s

|hr|

.. exec::
  
   s = "Hello, world."
   s



Reading code from a file
------------------------

Instead of inserting the code literally into the RST sources, you can also put it in a separate file.
The file path must be given relative to the top-level Sphinx directory (i.e. the directory which ``conf.py`` is in).
The contents of the file will be read in and executed in the same way.
As before, outputs must be printed to stdout.

.. code-block:: rst
   :caption: rst

   .. exec:: examples/hellofile.py

|hr|

.. exec:: examples/hellofile.py

