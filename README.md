# sphinx-exec-directive

Run Python code blocks and display the output directly within Sphinx documentation.

This is based very strongly on [matplotlib's `plot_directive` extension](https://matplotlib.org/stable/api/sphinxext_plot_directive_api.html?highlight=plot%20directive#module-matplotlib.sphinxext.plot_directive), but is used for running code instead of generating plots.

**Note:** This allows arbitrary code execution using [`exec()`](https://docs.python.org/3/library/functions.html#exec). Don't do silly things with it.


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


## Example usage

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

## Caching

Outputs are cached by default, UNLESS context preservation has been requested in any part of the same document (see #4 for rationale).
To turn this off on a per-codeblock basis (e.g. if the code depends on the time which it is run at), use the `:cache: false` option.

```
.. exec::
   :cache: false
   
   from datetime import datetime
   print(datetime.now())
```

## The `context` option

Use this to preserve objects between different `exec` directives.
Setting this to `true` (or `True` or `1` or `yes`) will keep any objects in the current exec directive "alive" for the next one.

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

![Example sphinx-exec-directive output using context flag](https://i.stack.imgur.com/FdvRm.png)
