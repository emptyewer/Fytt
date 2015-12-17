# -*- coding: utf-8 -*-
"""
First build the extension using

python setup.py build_ext --inplace

then...

py2app/py2exe build script for Fytt2.

Will automatically ensure that all build prerequisites are available
via ez_setup

Usage (Mac OS X):
   python setup.py py2app -O2

Usage (Windows):
   python setup.py py2exe

Usage (Linux):
pyinstaller -y -F fytt2.py -n Fytt -i Icon.ico (use dev version 2.1-dev from https://github.com/pyinstaller/pyinstaller)
"""
import os
import sys
if sys.platform == 'darwin':
    from distutils.core import setup
    import py2app
elif sys.platform == 'win32':
    from setuptools import setup
    import py2exe

# from distutils.extension import Extension
# from Cython.Distutils import build_ext
# import numpy as np

# ext_modules = [Extension("functions", ["functions.pyx"])]
#
# setup(
#   name='Test',
#   cmdclass={'build_ext': build_ext},
#   include_dirs=[np.get_include()],
#   ext_modules=ext_modules,
# )

APP = ['fytt2.py']
DATA_FILES = [('images', ['fytt-icon.png']), ('db', ['fytt2_db.sqlite3'])]
OPTIONS = {'argv_emulation': False,
           'iconfile' : 'Icon.icns',
           'plist': {'CFBundleGetInfoString': 'Fytt: Spectral decomposition by linear least squares fitting',
                     'CFBundleIdentifier': 'edu.uiowa.vkrishnamani.fytt2',
                     'CFBundleShortVersionString': '2.6',
                     'CFBundleName': 'Fytt',
                     'CFBundleVersion': '26',
                     'NSHumanReadableCopyright': '(c) 2015 Venkatramanan Krishnamani'},
            'includes': ['sip', 'PyQt4', 'PyQt4.QtCore', 'PyQt4.QtGui', 'numpy', 'scipy', 'pyqtgraph', 'sys', 're', 'threading'],
           }


sys.setrecursionlimit(100000)

if sys.platform == 'darwin':
  setup(
    app=APP,
    name='Fytt',
    data_files=DATA_FILES,
    options={'py2app': OPTIONS},
    setup_requires=['py2app'],
    author='Venkatramanan Krishnamani',
    author_email='venky.krishna@me.com',
  )
elif sys.platform == 'win32':
  setup(
    windows=[{"script":'fytt2.py',
               "icon_resources": [(1, "Icon.ico")],
               "dest_base":"Fytt"
            }],
    options={"py2exe":{"includes" :["scipy.sparse.csgraph._validation", "scipy.special._ufuncs_cxx", "scipy.integrate"],
                       "optimize": 2}}
  )