C++
===

C++ support is essentially the same as for :doc:`C <c>`, except that it uses ``g++`` or ``clang++`` as the compiler.

You can use compilation options, as well as a Makefile, in the same way that you can for C.


.. code-block:: rst
   :caption: rst

   .. exec::
      :language: cpp

      #include <iostream>
      int main() {
          std::cout << "Hello, world.\n";
      }

|hr|

.. exec::
   :language: cpp

   #include <iostream>
   int main() {
       std::cout << "Hello, world.\n";
   }
