# sphinx-exec-directive

`sphinx-exec-directive` allows you to write code blocks in reStructuredText files, execute them during Sphinx compilation, and display the output directly within the generated documentation.

The 'default' code language is Python, but there is some limited support for other languages right now.
Note that for other languages, you will need to have the corresponding executables on `$PATH`.
See: [Other Languages](#other-languages).

This is based very strongly on [matplotlib's `plot_directive` extension](https://matplotlib.org/stable/api/sphinxext_plot_directive_api.html?highlight=plot%20directive#module-matplotlib.sphinxext.plot_directive), but is used for running code instead of generating plots.

**Note:** This allows arbitrary code execution. Don't do silly things with it.

## Contents

 - [Installation](#installation)
 - [Basic usage: Python code blocks](#basic-usage-python-code-blocks)
 - [Reading code from a file](#reading-code-from-a-file)
 - [Other languages](#other-languages)
 - [Caching](#caching)
 - [Preserving context](#preserving-context)


## Installation

Install from PyPI:

```
pip install sphinx-exec-directive
```

or manually:

```
git clone https://github.com/yongrenjie/sphinx-exec-directive
cd sphinx-exec-directive
pip install .
```

Then, inside your Sphinx `conf.py`, add `sphinx_exec_directive` to your list of extensions (note: underscores not hyphens).

```
extensions = [
    sphinx_exec_directive,
    # other extensions...
]
```


## Basic usage: Python code blocks

A short example will suffice. Putting

```
.. exec::
   
   print(1 + 1)
```

into your RST file will generate two literal blocks, one with the 'input' source code, and one with the captured stdout.
It looks pretty basic, but it does the job:

![Example sphinx-exec-directive output](https://i.stack.imgur.com/5sVSS.png)

Note that objects **must** be printed to stdout, or they will not be displayed.
This behaviour therefore differs slightly from the functionality in a Jupyter notebook (where the last line is evaluated and the result displayed automatically), or the interactive Python console.
If nothing is printed to stdout (or only empty space is) then the output literal block will be omitted.

## Reading code from a file

Instead of inserting the code literally into the RST sources, you can also put it in a separate file.
The file path **must** be given relative to the top-level Sphinx directory (i.e. the directory which `conf.py` is in):

```
.. exec:: subfolder/my_script.py
```

The same conditions apply; anything you want to display must be printed to stdout.

## Other languages

A few other processes are available, for running code in different languages.
These all use the `:process: PROCESS` option, where `PROCESS` is one of the following.
For these to work, you will need to have certain executables present in your `PATH`.

| `PROCESS` | Requirements | Description |
| --------- | ------------ | ----------- |
| `haskell` | `runghc` or `ghci` or `cabal` or `stack` executables | Pipes the code into `runghc` or `ghci`, or calls a `cabal` or `stack` target and captures stdout. 
| `matlab`  | `matlab` executable | Creates a tempfile and runs non-interactive Matlab on it. |
| `shell`   |                     | Pipes the code into `sh`. Note that the initial working directory will be your home directory. |

I plan to generalise this (see [#7](https://github.com/yongrenjie/sphinx-exec-directive/issues/7)) in the future.

## Basic usage: Haskell code blocks

Haskell code can be run with `runghc`, `ghci`, or can run a `cabal` or `stack`
target and show its output:

### Run with runghc

Using `runghc` requires that the code block defines a module complete with a
`main` function:

```
.. exec::
   :context: false
   :process: haskell

   module Main where

   main :: IO ()
   main = do
     let x = fmap (+10) [1..10]
     print x
```

and this produces:

![Example sphinx-exec-directive output haskell-runghc](https://imgur.com/a/Fcc8vEg)

where the code block is shown and its output immediately follows. See
[Preserving context](#preserving-context) for information on the context flag.

### Run with ghci

Using `ghci` requires that `ghci` is on your `$PATH`. You should use this runner
when you want to show some type signatures or run code that is not affiliated
with a project. See the [Run with Cabal](#run-with-cabal) section for running
project targets or ghci loaded with your project:

```
.. exec::
   :context: true
   :process: haskell
   :with: ghci

   :t "Hello"
```

Notice the new `with` flag. This changes the default runner from `runghc` to
`ghci`. This invocation produces:

![Example sphinx-exec-directive output haskell-ghci](https://imgur.com/uAPvQYA)

an expected. We can also load any packages in the global environment into the
ghci instance:

```
.. exec::
   :context: true
   :process: haskell
   :with: ghci

   :m + Data.List
   :t span
```

Which produces: 

![Example sphinx-exec-directive output haskell-ghci-pkg](https://imgur.com/2ARnMpa)

### Run with Cabal or Stack

If you have a `cabal` or `stack` project that your documentation builds upon
then you can run any `cabal` or `stack` target and capture its output through
the `exec` directive. This is particularly useful for showing benchmarks in
text. For example the [Haskell Optimization
Handbook](https://github.com/input-output-hk/hs-opt-handbook.github.io) has a
cabal project whose programs are used to elucidate points made in the handbook.
So it runs benchmarks in the handbook to show off the effects of different
optimizations. The directive invocation becomes:

```
.. exec:: code/lethargy/bench/TooManyClosures.hs
   :context: true
   :process: haskell
   :project_dir: code/lethargy/
   :with: cabal
   :args: bench lethargy:tooManyClosures
```

 Notice the invocation takes a source file after `exec::` and that there are
 several new flags: `project_dir`, `with`, and `args`. `project_dir` is a
 _relative_ filepath that is relative to the root directory of the sphinx
 project (where your `conf.py` is located). `with` sets the runner to use
 `cabal` in this example, if you're using `stack` then `with` should be set to
 `stack`. `args` are all the arguments that you want to pass to either `cabal`
 or `stack`. The runner code is deliberately simple, it does not try to figure
 things out for you or hunt for your `.cabal` or `.stack` files. It simply
 aggregates the needed information, performs some safety checks, and runs either
 `cabal` or `stack` with the `args` field. This produces:

![Example sphinx-exec-directive output haskell-cabal](https://imgur.com/BMB9gDc)

Where the file is shown in its entirety, followed by the output of the `cabal`
or `stack` target. If you do not need to show the entire file then remove the
filepath after the `exec::` call. Notice that the output from the target only
shows the output _produced_ by the target, that is, it elides all output from
building the project and its dependencies. This is purposefully filtered and is
not exposed to the end-user (that's you) to disable. If you need this then
please open an issue!

## Caching

Outputs are cached by default, **unless** context preservation has been requested in any part of the same document (see [#4](https://github.com/yongrenjie/sphinx-exec-directive/issues/4) for rationale).
To turn this off on a per-codeblock basis (e.g. if the code depends on the time which it is run at), specify a falsy value for the `:cache` option.

```
.. exec::
   :cache: false
   
   from datetime import datetime
   print(datetime.now())
```

## Preserving context

Setting the `:context:` option to a truthy value will keep any objects in the current exec directive "alive" for the next one.
Note that this only works for Python blocks, and is incompatible with caching (see above).

```
.. exec::
   :context: true

   x = 5
   print(x)

Some other text goes here... Let's print x again...

.. exec::

   print(x)

It will work.

```

## Adding a paragraph between Python and output blocks

Setting the `:intertext:` option to a text inserts the text in between the Python and output blocks.
The text may use a basic reStructuredText syntax.

```
.. exec::
   :intertext: prints the value of the variable ``x``:

   x = 5
   print(x)
```

<!-- generate image for this -->
![Example sphinx-exec-directive output using intertext option](https://i.stack.imgur.com/FdvRm.png)
