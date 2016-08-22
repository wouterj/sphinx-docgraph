from setuptools import setup, find_packages

setup(
    name = 'sphinx-docgraph', 
    version = '1.0',
    author = 'Wouter de Jong',
    author_email = 'wouter@wouterj.nl',
    description = 'Sphinx builder to visualize doctrees',
    license = 'BSD-2-Clause',
    packages = find_packages(),
    install_requires = ['Sphinx']
)
