#!/usr/bin/env python

from setuptools import setup, find_packages

import os

import versioneer
from versioneer import get_cmdclass
sdist = get_cmdclass()['sdist']
build_py = get_cmdclass()['build_py']

here = os.path.dirname(os.path.abspath(__file__))
node_root = os.path.join(here, 'js')
is_repo = os.path.exists(os.path.join(here, '.git'))




CLASSIFIERS = [
    "Development Status :: 3 - Alpha",
    "Intended Audience :: Science/Research",
    "Intended Audience :: Developers",
    "License :: OSI Approved :: MIT License",
    "Programming Language :: JavaScript",
    "Programming Language :: Python",
    "Programming Language :: Python :: 2",
    "Programming Language :: Python :: 3",
    "Topic :: Scientific/Engineering :: Bio-Informatics",
    "Topic :: Scientific/Engineering :: Chemistry",
    "Topic :: Scientific/Engineering :: Visualization",
    "Operating System :: POSIX",
    "Operating System :: Unix",
    "Operating System :: MacOS",
]



setup_args = {
    'name': 'MDsrv',
    'version': versioneer.get_version(),
    'description': 'Server for coordinate trajectories from molecular dynamics simulations.',
    'include_package_data': True,
    'package_data': {
         "mdsrv.data": ["*"]
     },
    'license': "MIT",
    'entry_points': {'console_scripts':
          ['mdsrv = mdsrv:entry_point',]
    },
    'setup_requires': {
        "cython": ["cython"],
        "numpy": ["numpy"],
        "scipy": ["scipy"],
        "setuptools": ["setuptools"],
        "flask": ["flask"],
    },
    'install_requires': {
        "mdtraj": ["mdtraj"],

    },
    'extra_requires': {
        "mdanalysis;platform_system!='Windows' and python_version<'3.4'": ["mdanalysis"],
    },
    'packages': set(find_packages() + 
                ['mdsrv']),
    'zip_safe': False,
    'cmdclass': versioneer.get_cmdclass(),
    'author': 'Alexander S. Rose, Johanna K. S. Tiemann',
    'author_email': 'alexander.rose@weirdbyte.de, johanna.tiemann@gmail.com',
    'url': 'https://github.com/arose/mdsrv',
    'keywords': [
        'Molecular Dynamics simulation',
    ],
    'classifiers': CLASSIFIERS,
}


setup(**setup_args)
