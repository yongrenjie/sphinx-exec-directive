Haskell
=======

Haskell code can be run with ``runghc`` or ``ghci``.
Alternatively, it is also possible to run a ``cabal`` or ``stack`` target and show its output.

Using ``runghc`` (default)
--------------------------

Using ``runghc`` requires that the code block defines a module complete with a
``main`` function:

.. code-block:: rst
   :caption: rst

   .. exec::
      :language: haskell

      module Main where

      main :: IO ()
      main = do
        let x = fmap (+10) [1..10]
        print x

|hr|

.. exec::
   :language: haskell

   module Main where

   main :: IO ()
   main = do
     let x = fmap (+10) [1..10]
     print x


Using ``ghci``
--------------

Using ``ghci`` requires that ``ghci`` is on your ``$PATH``.
You should use this runner when you want to show some type signatures or run code that is not affiliated with a project.
See the :ref:`Cabal <haskell-cabal>` section for running project targets or ``ghci`` loaded with your project.

Notice the new ``with`` flag here: this changes the default runner from ``runghc`` to ``ghci``.

``.ghci`` files are ignored by this runner (this makes results more reproducible).

.. code-block:: rst
   :caption: rst

   .. exec::
      :language: haskell
      :with: ghci

      :t "Hello"

|hr|

.. exec::
   :language: haskell
   :with: ghci
 
   :t "Hello"

You can also load any packages in the global environment into the ``ghci`` instance:

.. code-block:: rst
   :caption: rst

   .. exec::
      :language: haskell
      :with: ghci
   
      :m + Data.List
      :t span

|hr|

.. exec::
  :language: haskell
  :with: ghci

  :m + Data.List
  :t span


.. _haskell-cabal:

Running Cabal or Stack projects
-------------------------------

If you have a ``cabal`` or ``stack`` project that your documentation builds upon, then you can run any ``cabal`` or ``stack`` target and capture its output.
As a simple example, here's a project that was generated just using ``cabal init``.

.. code-block:: rst
   :caption: rst

   .. exec:: examples/hellocabal/app/Main.hs
      :language: haskell
      :with: cabal
      :args: run hellocabal
      :project_dir: examples/hellocabal

|hr|

.. exec:: examples/hellocabal/app/Main.hs
   :language: haskell
   :with: cabal
   :args: run hellocabal
   :project_dir: examples/hellocabal

In this case, ``cabal`` is simply run with the given command-line arguments (``:args:``), in the *project directory* specified using the ``:project_dir:`` option.
The project directory must be specified relative to the top-level Sphinx directory, and is mandatory.
The arguments can be empty, but that won't be very useful because you'll be running a bare command ``cabal``.
The ``with`` option sets the runner to use ``cabal`` in this example; if you're using ``stack`` then you can analogously use ``with: stack``.

The source file does not need to be specified; it isn't actually executed, and is only used to show the source code being run.
You may find that this is not really necessary, in which case the filename can simply be left out (the output of running the ``cabal``/``stack`` command will still remain).

The runner code is deliberately simple; it does not try to figure things out for you or hunt for your ``.cabal`` or ``.stack`` files.
It simply aggregates the needed information, performs some safety checks, and runs either ``cabal`` or ``stack`` with the ``args`` field.
Notice that the output from the target only shows the output *produced* by the target, that is, it elides all output from building the project and its dependencies.
This is purposely filtered and is not exposed to the end-user (that's you) to disable.
If you need this, please `open an issue <https://github.com/yongrenjie/sphinx-exec-directive/issues>`_.

One thing this is particularly useful for is showing benchmarks in text.
For example, the `Haskell Optimization Handbook <https://github.com/input-output-hk/hs-opt-handbook.github.io>`_ has a ``cabal`` project whose programs are used to elucidate points made in the handbook.
So, it runs benchmarks in the handbook to show off the effects of different optimisations.
The directive invocation becomes:

.. code-block:: rst
   :caption: rst

   .. exec:: code/lethargy/bench/TooManyClosures.hs
      :language: haskell
      :with: cabal
      :args: bench lethargy:tooManyClosures
      :project_dir: code/lethargy/

The output is shown `here <https://imgur.com/BMB9gDc>`_.
