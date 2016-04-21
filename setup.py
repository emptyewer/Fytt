# -*- coding: utf-8 -*-
"""
First build the extension using

python setup.py build_ext --inplace

then...

py2app/py2exe build script for Fytt.

Will automatically ensure that all build prerequisites are available
via ez_setup

Usage (Mac OS X):
   /usr/bin/python setup.py py2app -O2

Usage (Windows):
   python setup.py py2exe

Usage (Linux):
pyinstaller -y -F fytt.py -n Fytt -i Icon.ico (use dev version 2.1-dev from https://github.com/pyinstaller/pyinstaller)
"""
import os
import glob
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


def find_data_files(sources, targets, patterns):
    """Locates the specified data-files and returns the matches
    in a data_files compatible format.

    source is the root of the source data tree.
        Use '' or '.' for current directory.
    target is the root of the target data tree.
        Use '' or '.' for the distribution directory.
    patterns is a sequence of glob-patterns for the
        files you want to copy.
    """

    ret = {}
    for i, source in enumerate(sources):
        target = targets[i]
        if glob.has_magic(source) or glob.has_magic(target):
            raise ValueError("Magic not allowed in src, target")
        pattern = os.path.join(source, patterns[i])
        for filename in glob.glob(pattern):
            if os.path.isfile(filename):
                targetpath = os.path.join(target, os.path.relpath(filename, source))
                path = os.path.dirname(targetpath)
                ret.setdefault(path, []).append(filename)
    return sorted(ret.items())

APP = ['fytt.py']
DATA_FILES = [('images', ['fytt-icon.png']), ('', ['fytt_db.sqlite3']), ('ui', ['ui/info.ui'])]
OPTIONS = {'argv_emulation': False,
           'iconfile' : 'Icon.icns',
           'plist': {'CFBundleGetInfoString': 'Fytt: Spectral decomposition by linear least squares fitting',
                     'CFBundleIdentifier': 'edu.uiowa.vkrishnamani.fytt',
                     'CFBundleShortVersionString': '2.6.1',
                     'CFBundleName': 'Fytt',
                     'CFBundleVersion': '261',
                     'NSHumanReadableCopyright': '(c) 2016 Venkatramanan Krishnamani'},
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
    origIsSystemDLL = py2exe.build_exe.isSystemDLL
    def isSystemDLL(pathname):
            if os.path.basename(pathname).lower() in ("msvcp71.dll", "dwmapi.dll", "'msvcp90.dll'"):
                    return 0
            return origIsSystemDLL(pathname)
    py2exe.build_exe.isSystemDLL = isSystemDLL
    setup(
        windows=[{"script":'fytt.py',
               "icon_resources": [(1, "Icon.ico")],
               "dest_base":"Fytt"
            }],
        data_files=DATA_FILES,
        options={"py2exe": {"includes" :["scipy.sparse.csgraph._validation", "scipy.special._ufuncs_cxx", "scipy.integrate",
                                     'scipy', 'scipy.integrate', 'scipy.special.*','scipy.linalg.*', "scipy.misc", "scipy.linalg.cython_blas"],
                        "optimize": 2,
                        "bundle_files": 1,
                        "compressed": 2}}
    )