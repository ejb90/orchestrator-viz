# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = 'orchestrator-viz'
copyright = '2025, ejb90'
author = 'ejb90'
release = '0.1.0'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    'sphinx.ext.autodoc',   # Add autodoc extension
    'sphinx.ext.napoleon',  # Support for NumPy and Google style docstrings
    'sphinx.ext.viewcode',  # Add links to view the source code
    'sphinx.ext.doctest',   # Support for doctests in docstrings
    'sphinx_rtd_theme',     # Modern style
    ]
templates_path = ['_templates']
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'sphinx_rtd_theme'  # Use the Read the Docs theme
html_static_path = ['_static']

# -- Napoleon settings -------------------------------------------------------
napoleon_google_docstring = True  # Enable Google style docstrings
napoleon_numpy_docstring = True   # Enable NumPy style docstrings
napoleon_include_init_with_doc = True  # Include __init__ docstring
napoleon_include_private_with_doc = False  # Don't include private members
napoleon_include_special_with_doc = True  # Include special members
napoleon_use_admonition_for_examples = True  # Use admonition for examples
napoleon_use_admonition_for_notes = True  # Use admonition for notes
napoleon_use_admonition_for_references = True  # Use admonition for references
napoleon_use_ivar = True  # Use :ivar: for instance variables
napoleon_use_param = True  # Use :param: for parameters
napoleon_use_rtype = True  # Use :rtype: for return type