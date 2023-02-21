Other languages
===============

Some support for other languages is present (I plan to extend this in the future).
The language to be used is specified with the ``:process: PROCESS`` option, where ``PROCESS`` is one of the following.
Generally, to run code blocks of other languages, you will need to have the relevant executable(s) installed and locatable in ``$PATH``.

For more information, follow the links for the respective languages below.

.. list-table::
   :header-rows: 1

   * - ``PROCESS``
     - Required executables
     - Description

   * - :doc:`haskell <haskell>`
     - ``runghc``, ``ghci``, ``cabal``, or ``stack``
     - Pipes the code into ``runghc`` or ``ghci``, or calls a ``cabal`` or ``stack`` target and captures stdout

   * - ``matlab``
     - ``matlab``
     - Creates a tempfile and runs non-interactive Matlab on it

   * - ``shell``
     - ``sh``
     - Pipes the code into ``sh``; note that the initial working directory will be your home directory


..
   This hidden toctree directive is needed to silence warnings about the
   individual language pages not being included in any toctree.

.. toctree::
   :hidden:

   haskell
