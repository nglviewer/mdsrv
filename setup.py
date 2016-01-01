#!/usr/bin/env python

from setuptools import setup

if __name__ == '__main__':
    setup(
        name = "MDsrv",
        version = "0.1dev",
        author = "Alexander S. Rose",
        description = "Server for coordinate trajectories from molecular dynamics simulations",
        py_modules = [ 'mdsrv' ],
        license = "MIT",
        url = "https://github.com/arose/mdsrv",
        zip_safe = False,
        install_requires = [ "Flask", "simpletraj" ],
        entry_points = {
            "console_scripts": [
                'mdsrv = mdsrv:entry_point'
            ]
        }
    )
