# Configuration file for the Sphinx documentation builder.
import os
import sys

# Add griot-core to path
sys.path.insert(0, os.path.abspath('../src'))

# Project information
project = 'griot-core'
copyright = '2026, Griot Project'
author = 'Griot Team'
release = '0.8.0'

# Extensions
extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.napoleon',
    'sphinx.ext.viewcode',
    'sphinx.ext.intersphinx',
    'sphinx_copybutton',
]

# Templates and static
templates_path = ['_templates']
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']

# HTML output
html_theme = 'furo'
html_static_path = ['_static']

# Autodoc settings
autodoc_member_order = 'bysource'
autodoc_typehints = 'description'

# Napoleon settings
napoleon_google_docstring = True
napoleon_numpy_docstring = True
napoleon_include_init_with_doc = True

# Mock imports for modules that may not be available
autodoc_mock_imports = [
    'wasmtime',
    'pyarrow',
    'flask',
    'boto3',
    'kubernetes',
    'google',
    'httpx',
    'prefect',
    'dagster',
    'airflow',
]

# Intersphinx
intersphinx_mapping = {
    'python': ('https://docs.python.org/3', None),
}
