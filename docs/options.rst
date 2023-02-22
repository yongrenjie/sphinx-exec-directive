Options
=======

This page explains some of the available options.
There aren't many at this point in time; if you'd like a feature please `open an issue <https://github.com/yongrenjie/sphinx-exec-directive/issues>`_.


Caching
-------

By default, outputs are cached, *unless* context preservation has been requested in any part of the same document.
To turn this off on a per-codeblock basis (e.g. if the code depends on the time which it is run at), specify a falsy value for the ``:cache:`` option.
For example, what you'll see in the stdout block here is the last time the documentation was built.

.. code-block:: rst
   :caption: rst

   .. exec::
      :cache: false

      from datetime import datetime
      print(datetime.now())

|hr|

.. exec::
   :cache: false

   from datetime import datetime
   print(datetime.now())


Context preservation
--------------------

The ``:context:`` option can be used to preserve variables between Python code blocks in the same file.
This has no effect on other languages, and is incompatible with caching.

For example, you can define a variable in the first code block:

.. code-block:: rst
   :caption: rst

   .. exec::
      :context: true

      x = 5
      print(f'x is equal to {x}')

|hr|

.. exec::
   :context: true

   x = 5
   print(f'x is equal to {x}')

You can later print the value of ``x`` again:

.. code-block:: rst
   :caption: rst

   .. exec::

      print(f'x is *still* equal to {x}')

|hr|

.. exec::

   print(f'x is *still* equal to {x}')

Note that these variables are cleared upon encountering any code block where the ``context`` option is not explicitly enabled.
So, if we were to try to print ``x`` again at this point, it would fail, because the block immediately above this did not use the ``context`` option.

If this option is enabled, context for Python code blocks will always be carried through code blocks of other languages.


Interspersed text
-----------------

The ``:intertext:`` option may be used to insert text between the code and stdout blocks.
Basic RST syntax can be used.

.. code-block:: rst
   :caption: rst

   This code

   .. exec::
      :intertext: prints the value of the variable ``x``:

      x = 5
      print(x)

|hr|

This code

.. exec::
  :intertext: prints the value of the variable ``x``:

  x = 5
  print(x)

