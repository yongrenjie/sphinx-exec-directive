# sphinx-exec-directive

`sphinx-exec-directive` allows you to write code blocks in reStructuredText files, execute them during Sphinx compilation, and display the output directly within the generated documentation.

The 'default' code language is Python, but there is some limited support for other languages right now (see the documentation for more info).

This is based very strongly on [matplotlib's `plot_directive` extension](https://matplotlib.org/stable/api/sphinxext_plot_directive_api.html?highlight=plot%20directive#module-matplotlib.sphinxext.plot_directive), but is used for running code instead of generating plots.


## Installation

```
pip install sphinx-exec-directive
```

Then, inside your Sphinx `conf.py`, add `sphinx_exec_directive` to your list of extensions (note: underscores not hyphens).

```
extensions = [
    sphinx_exec_directive,
    # other extensions...
]
```

## Basic example

```
.. exec::
   
   print(1 + 1)
```

Place the above into your RST file and Sphinx will generate two literal blocks when compiling, one with the 'input' source code, and one with the captured stdout:

![Example sphinx-exec-directive output](https://i.stack.imgur.com/5sVSS.png)


## Documentation

For further details and usage examples, please see the [documentation](https://yongrenjie.github.io/sphinx-exec-directive).
It contains quite a few exec directives, so you get to see some in the wild!
