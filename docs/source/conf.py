# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Add project roots to PATH -----------------------------------------------

import os
import sys

# Get current working directory
cwd = os.getcwd()
# Get the root dir by going back two times
project_root = os.path.dirname(os.path.dirname(cwd))
# Add the root dir to the system path
sys.path.insert(0, project_root)

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = "Delivery Fee Calculator Flask App"
copyright = "2024, Mamdasan Sabrian"
author = "Mamdasan Sabrian"
version = "1.0"
release = "1.0.0-alpha"

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

# Enable autodoc extension for automatic documentation generation.
extensions = [
    "sphinx.ext.autodoc",
]

# Specify the location of template files.
templates_path = ["_templates"]

# Specify any patterns for excluding specific files or directories.
exclude_patterns = []

# The suffix of source filenames.
source_suffix = ".rst"

# The master toctree document.
master_doc = "index"

# The name of the Pygments (syntax highlighting) style to use.
pygments_style = "sphinx"

# Set sorting of methods based on the source (default is alphabetical)
autodoc_member_order = "bysource"

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = "alabaster"
html_static_path = ["_static"]
