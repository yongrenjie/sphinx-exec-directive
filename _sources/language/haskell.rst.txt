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
      :process: haskell

      module Main where

      main :: IO ()
      main = do
        let x = fmap (+10) [1..10]
        print x

|hr|

.. exec::
   :process: haskell

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
      :process: haskell
      :with: ghci

      :t "Hello"

|hr|

.. exec::
   :process: haskell
   :with: ghci
 
   :t "Hello"

You can also load any packages in the global environment into the ``ghci`` instance:

.. code-block:: rst
   :caption: rst

   .. exec::
      :process: haskell
      :with: ghci
   
      :m + Data.List
      :t span

|hr|

.. exec::
  :process: haskell
  :with: ghci

  :m + Data.List
  :t span


.. _haskell-cabal:

Running with Cabal or Stack
---------------------------

If you have a ``cabal`` or ``stack`` project that your documentation builds upon, then you can run any ``cabal`` or ``stack`` target and capture its output.
This is particularly useful for showing benchmarks in text.
For example, the `Haskell Optimization Handbook <https://github.com/input-output-hk/hs-opt-handbook.github.io>`_ has a ``cabal`` project whose programs are used to elucidate points made in the handbook.
So, it runs benchmarks in the handbook to show off the effects of different optimisations.
The directive invocation becomes:

.. code-block:: rst
   :caption: rst

   .. exec:: code/lethargy/bench/TooManyClosures.hs
      :process: haskell
      :project_dir: code/lethargy/
      :with: cabal
      :args: bench lethargy:tooManyClosures

(The output is shown `here <https://imgur.com/BMB9gDc>`_.)

Notice the invocation takes a source file after ``exec::``, and that there are several new flags: ``project_dir``, ``with``, and ``args``.
``project_dir`` is a *relative* filepath that is relative to the root directory of the Sphinx
project (where your ``conf.py`` is located).
The ``with`` option sets the runner to use ``cabal`` in this example; if you're using ``stack`` then you can analogously use ``with: stack ``.
Finally, ``args`` are just all the command-line arguments that you want to pass to either ``cabal`` or ``stack``.

The runner code is deliberately simple; it does not try to figure things out for you or hunt for your ``.cabal`` or ``.stack`` files.
It simply aggregates the needed information, performs some safety checks, and runs either ``cabal`` or ``stack`` with the ``args`` field.

The source file is shown in its entirety, followed by the output of the ``cabal`` or ``stack`` target.
If you do not need to show the entire file, then remove the filepath after the ``exec::`` call.
Notice that the output from the target only shows the output *produced* by the target, that is, it elides all output from building the project and its dependencies.
This is purposely filtered and is not exposed to the end-user (that's you) to disable.
If you need this then please `open an issue <https://github.com/yongrenjie/sphinx-exec-directive/issues>`_!
