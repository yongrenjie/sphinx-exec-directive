OCaml
=====

OCaml code can be run in one of three ways:

 - Directly as a script (see https://v2.ocaml.org/manual/toplevel.html)
 - By piping into the ``utop`` toplevel (REPL).
   This lets you get, for example, type signatures.
 - Running a target in a ``dune`` project.


As a script
-----------

In the first option, the code is placed in a temporary file and run using the ``ocaml`` executable.

.. code-block:: rst
   :caption: rst

   .. exec::
      :language: ocaml

      let rec fact n = if n = 0 then 1 else n * fact (n - 1);;

      fact 5 |> print_int

|hr|

.. exec::
   :language: ocaml

   let rec fact n = if n = 0 then 1 else n * fact (n - 1);;

   fact 5 |> print_int


Piping into ``utop``
--------------------

To do this, you will need to use the ``:with: utop`` option.
Don't forget the ``;;`` expression terminators!
This is the same code as before, but notice that type information is shown.

.. code-block:: rst
   :caption: rst

   .. exec::
      :language: ocaml
      :with: utop

      let rec fact n = if n = 0 then 1 else n * fact (n - 1);;
      fact 5;;

|hr|

.. exec::
   :language: ocaml
   :with: utop

   let rec fact n = if n = 0 then 1 else n * fact (n - 1);;
   fact 5;;


Running Dune projects
---------------------

To run a ``dune`` project, specify ``:with: dune`` and the remaining arguments to be passed to ``dune`` in the ``:args:`` option.

When using this, it is also mandatory to specify a *project directory* using ``:project_dir:``.
This path is the folder in which ``dune`` will be run, and should be specified relative to the top-level Sphinx directory (i.e. the directory that ``conf.py`` is in).

The filepath after ``.. exec::`` is completely optional: if you specify it, the source code of that file will be shown, but it otherwise does not affect the output (which is obtained purely by running the specified ``dune`` command).


.. code-block:: rst
   :caption: rst

   .. exec:: examples/hellodune/hellodune.ml
      :language: ocaml
      :with: dune
      :args: exec hellodune
      :project_dir: examples/hellodune

|hr|

.. exec:: examples/hellodune/bin/main.ml
   :language: ocaml
   :with: dune
   :args: exec hellodune
   :project_dir: examples/hellodune
