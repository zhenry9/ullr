# Configuration file for the Sphinx documentation builder.
#
# This file only contains a selection of the most common options. For a full
# list see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Path setup --------------------------------------------------------------

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
#
import os
import sys
# sys.path.insert(0, os.path.abspath('......\AppData\Local\Programs\Python\Python39\Lib\site-packages'))
sys.path.append('.')
from links.link import *
from links import *

# -- Project information -----------------------------------------------------

project = 'Ullr'
copyright = '2021, Zach Henry'
author = 'Zach Henry'

# The full version, including alpha/beta/rc tags
release = "0.1.2"


# -- General configuration ---------------------------------------------------

import sphinx_rtd_theme

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [ 
    'recommonmark',
    'sphinx_markdown_tables',
    'sphinx.ext.autosectionlabel',
    'hoverxref.extension',
    'sphinx_rtd_theme',
    ]

# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = []


# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
html_theme = 'sphinx_rtd_theme'

html_favicon = 'favicon-32x32.png'

# html_logo = 'mammoth-logo.jpg'

# Theme options are theme-specific and customize the look and feel of a theme
# further.  For a list of options available for each theme, see the
# documentation.
html_theme_options = {
    "collapse_navigation" : False
}

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ['_static']

# html_css_files = [
#    'custom1.css',
#    ]

hoverxref_auto_ref = True

hoverxref_roles = [
    'term',
    ]

latex_elements = {
    'preamble': '\setcounter{tocdepth}{2}'
    }