C
==

Support for C is somewhat rudimentary.
The code is run by saving it to a tempfile, then calling ``gcc {filename} && ./a.out``.

If you prefer ``clang``, you can use the ``:with: clang`` option.

If you have a somewhat complicated project, it's probably better to use a Makefile (see below).

.. code-block:: rst
   :caption: rst

   .. exec::
      :language: c

      #include <stdio.h>
      int main() {
          printf("Hello, world.\n");
      }

|hr|

.. exec::
   :language: c

   #include <stdio.h>
   int main() {
       printf("Hello, world.\n");
   }


Compilation options
-------------------

You can use ``:args:`` to pass any options you want:

.. code-block:: rst
   :caption: rst

   .. exec::
      :language: c
      :args: -DDEBUG

      #include <stdio.h>
      int main() {
          #ifdef DEBUG
              printf("Debugging enabled!");
          #endif
      }

|hr|

.. exec::
  :language: c
  :args: -DDEBUG

  #include <stdio.h>
  int main() {
      #ifdef DEBUG
          printf("Debugging enabled!");
      #endif
  }


Using a Makefile
----------------

Assuming you have a somewhat complicated compilation setup, you can instead set up a Makefile and use that.
For example, the block below runs ``make all`` in the specified directory.
The filepath after ``.. exec::`` is completely optional: it's only needed if you want to show the source code of a particular file.

``make`` echoes the commands on top of running them.
If you don't want this, append ``-s`` to the ``:args:`` option.

.. code-block:: rst
   :caption: rst

   .. exec:: examples/hellomake/hellomake.c
      :language: c
      :with: make
      :args: all
      :project_dir: examples/hellomake

|hr|

.. exec:: examples/hellomake/hellomake.c
   :language: c
   :with: make
   :args: all
   :project_dir: examples/hellomake
