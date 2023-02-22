Matlab
======

GNU Octave is not supported, but in principle it can be (please open an issue if you need it).

Matlab code is run by dumping the code to a tempfile, and then executing ``matlab`` in batch mode on the tempfile.
Note that this requires that you have the ``matlab`` executable on your ``$PATH``, which may not have been set up by default.
For example, on a typical macOS installation, you need to append the folder ``/Applications/MATLAB_R2023a.app/bin`` to ``$PATH``.
I've never tried on Linux, but there are some instructions `here <https://uk.mathworks.com/help/matlab/matlab_env/start-matlab-on-linux-platforms.html>`_.

In this example, I'm running Matlab R2023a which (at the time of writing) is prerelease.
For release versions you won't see the header.

.. code-block:: rst
   :caption: rst

   .. exec::
      :language: matlab

      [1, 2, 3] + [4, 5, 6]
      [1, 2, 3] .* [4, 5, 6]

|hr|

.. exec::
   :language: matlab
  
   [1, 2, 3] + [4, 5, 6]
   [1, 2, 3] .* [4, 5, 6]
