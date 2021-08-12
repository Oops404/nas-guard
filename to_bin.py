# -*- coding: utf-8 -*-

from distutils.core import setup
from Cython.Build import cythonize

setup(name='nas_guard', ext_modules=cythonize(["nas_guard_py3.py", ]), )
