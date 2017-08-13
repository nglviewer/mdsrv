
[![License](http://img.shields.io/badge/license-MIT-blue.svg?style=flat)](LICENSE)
[![Version](http://img.shields.io/badge/version-0.3.5-blue.svg?style=flat)](https://github.com/arose/mdsrv/releases/tag/v0.3.5)
[![Changelog](https://img.shields.io/badge/changelog--lightgrey.svg?style=flat)](CHANGELOG)
[![Travis Build Status](https://travis-ci.org/arose/mdsrv.svg?branch=master)](https://travis-ci.org/arose/mdsrv)


MDsrv is a simple server that enables remote access to coordinate trajectories from molecular dynamics simulations. It can be used together with the NGL Viewer (http://github.com/arose/ngl) to interactively view trajectories of molecular complexes in a web-browser, either within a local network or from anywhere over the internet.

See it in action:
* [Web application](http://nglviewer.org/mdsrv/examples)
* [Documentation](http://nglviewer.org/mdsrv/)


Features
--------

* Coordinate trajectories (animation, remote access)
* Trajectory formats supported (xtc/trr, nc/netcdf, dcd, lammpstrj, xyz, binpos, hdf5, dtr, arc, tng)
* Additional trajectory formats supported - only unix with py2 (mdcrd/crd, dms,
trj, ent ncdf)
* [NGL Viewer](https://github.com/arose/ngl/) (Molecular structures, Density volumes, User interaction, Embeddable)
* Lightweight coordinate-only trajecotry reader (via [MDTraj](http://mdtraj.org/) and [MDAnalysis](http://www.mdanalysis.org/) )



Table of contents
=================

* [Documentation](#documentation)
* [RESTful API](#restful-api)
* [NGL browser support](#ngl browser-support)
* [Acknowledgments](#acknowledgments)
* [Cite](#cite)


Documentation
============

Detailed information concerning the installation, deployment, usage and scripting examples can be found at the [documentation](http://nglviewer.org/mdsrv/).


Installation
============

From PyPI:

    pip install mdsrv
    
From conda:
    conda config --add channels conda-forge
    conda install -c ngl mdsrv


MDsrv depends on MDtraj. Please ensure that this is installed correctly and functional.


Running
=======

The `mdsrv` command starts a local server and opens a browser window with the web application.

To use a custom configuration file

    mdsrv --cfg my_conf.cfg


Load a topology and trajectory at startup

    mdsrv struc.gro traj.xtc

For more options, please consult [the documentation](http://nglviewer.org/mdsrv)

Configuration file
------------------

Optional. Copy/rename the sample [app.cfg](app.cfg.sample) file. It allows e.g. setting `data_dir` data directories that will be accessible through the web server and to define access restrictions.


Deployment
==========

The Apache Webserver can used to run the server via `mod_wsgi`. First make sure you have everything required installed:

    sudo apt-get install apache2 libapache2-mod-wsgi


Then you need to create a wsgi configuration file to be referenced in the Apache configuration. There is an example named [mdsrv.wsgi.sample](mdsrv.wsgi.sample) in the root directory of this package. Also, a snippet showing how the configuration for Apache should look like can be found in the [apache.config.sample](apache.config.sample) file.

Finally, to restart apache issue

    sudo /etc/init.d/apache2 restart

More information can be found at the [documentation](http://nglviewer.org/mdsrv/).

RESTful API
===========

The RESTful API is the interface through which the web application gets all data but it may be also used to access the served trajectory data from other applications.

You can retrieve information about directory content (e.g. name of sub-directory, file name, file size), number of frames and frame coordinates.

For more information, please visit the [documentation](http://nglviewer.org/mdsrv/).

NGL browser support
===============

The NGL Viewer requires your browser to support WebGL. To see if your browser supports WebGL and what you might need to do to activate it, visit the [Get WebGL](https://get.webgl.org/) page.

Generally, WebGL is available in recent browser versions of Mozilla Firefox (>29) or Google Chrome (>27). The Internet Explorer supports WebGL only since version 11. The Safari Browser since version 8 (though WebGL can be activated in earlier version: first enable the Develop menu in Safari’s Advanced preferences, then secondly in the now visible Develop menu enable WebGL).

See also [this page](https://www.khronos.org/webgl/wiki/BlacklistsAndWhitelists) for details on which graphics card drivers are supported by the browsers.

__WebGL draft extensions__: For a smoother appearance of cylinders and spheres your browser needs to have the `EXT_frag_depth` extension available. The [WebGL Report](http://webglreport.com/) should list the extension if active. If not, you can enable WebGL draft extensions in your browser following these instructions:

* Chrome: browse to `about:flags`, enable the `Enable WebGL Draft Extensions` option, then relaunch.
* Firefox: browse to `about:config` and set `webgl.enable-draft-extensions` to `true`.
* Safari: Currently, the `EXT_frag_depth` extension is not supported.
* Internet Explorer: Currently, the `EXT_frag_depth` extension is not supported.




Acknowledgments
===============

Thanks to code from MDAnalysis (http://www.mdanalysis.org/) there is random access to xtc/trr trajectory files via indexing and seeking capabilities added to the libxdrfile2 library.


Funding sources:

* NCI/NIH award number U01 CA198942
* DFG project HI 1502
* HLRN project bec00085


Cite
====

When using MGsrv please cite:

* A. S. Rose, and MDsrv Contributors. MDsrv v0.2 Zenodo (2016), doi:10.5281/zenodo.45961.  [doi:10.5281/zenodo.45961](http://dx.doi.org/10.5281/zenodo.45961)
* AS Rose, AR Bradley, Y Valasatava, JM Duarte, A Prlić and PW Rose. _Web-based molecular graphics for large complexes._ ACM Proceedings of the 21st International Conference on Web3D Technology (Web3D '16): 185-186, 2016. [doi:10.1145/2945292.2945324](http://dx.doi.org/10.1145/2945292.2945324)
* AS Rose and PW Hildebrand. _NGL Viewer: a web application for molecular visualization._ Nucl Acids Res (1 July 2015) 43 (W1): W576-W579 first published online April 29, 2015. [doi:10.1093/nar/gkv402](https://doi.org/10.1093/nar/gkv402)
* RT McGibbon, KA Beauchamp, MP Harrigan, C Klein, JM Swails, CX Hernández, CR Schwantes, LP Wang, TJ Lane, VS Pande. _MDTraj: A Modern Open Library for the Analysis of Molecular Dynamics Trajectories._ Biophys J. (20 October 2015) 109(8):1528-32. [doi: 10.1016/j.bpj.2015.08.015](http:/dx.doi.org/10.1016/j.bpj.2015.08.015)
