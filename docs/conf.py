project = 'sphinx-exec-directive'
copyright = '2022–2023, Jonathan Yong'
author = 'Jonathan Yong & contributors'

extensions = ['sphinx_exec_directive', 'sphinx.ext.autosectionlabel']
root_doc = 'index'
exclude_patterns = []

html_theme = 'alabaster'
autosectionlabel_prefix_document = True

rst_prolog = """
.. |hr| raw:: html

   <hr />
"""
