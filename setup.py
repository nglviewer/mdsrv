#!/usr/bin/env python

from setuptools import setup


VERSION = "0.1dev"
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
    "Operating System :: Microsoft :: Windows",
    "Operating System :: POSIX",
    "Operating System :: Unix",
    "Operating System :: MacOS",
]


if __name__ == '__main__':
    setup(
        name = "MDsrv",
        author = "Alexander S. Rose",
        author_email = "alexander.rose@weirdbyte.de",
        description = "Server for coordinate trajectories from molecular dynamics simulations",
        version = VERSION,
        classifiers = CLASSIFIERS,
        license = "MIT",
        url = "https://github.com/arose/mdsrv",
        zip_safe = False,
        include_package_data = True,  # use MANIFEST.in during install
        packages = [ "mdsrv" ],
        install_requires = [ "Flask", "simpletraj" ],
        entry_points = {
            "console_scripts": [
                'mdsrv = mdsrv:entry_point'
            ]
        }
    )
