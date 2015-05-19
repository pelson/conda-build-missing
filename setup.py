#!/usr/bin/env python
import os
from distutils.core import setup

setup(name='conda_build_missing',
      version='1.0',
      author='Phil Elson',
      author_email='pelson.pub@gmail.com',
      packages=['conda_build_missing'],
      scripts=[os.path.join('conda-build-missing')],
     )
