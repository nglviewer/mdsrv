
[![License](http://img.shields.io/badge/license-MIT-blue.svg?style=flat)](LICENSE)
[![Version](http://img.shields.io/badge/version-0.2-blue.svg?style=flat)](https://github.com/arose/mdsrv/releases/tag/v0.2)
[![Changelog](https://img.shields.io/badge/changelog--lightgrey.svg?style=flat)](CHANGELOG)


MDsrv is a simple server that enables remote access to coordinate trajectories from molecular dynamics simulations. It can be used together with the NGL Viewer (http://github.com/arose/ngl) to interactively view trajectories of molecular complexes in a web-browser, either within a local network or from anywhere over the internet.

See it in action:
* [Web application](http://proteinformatics.charite.de/ngl/html/mdsrv.dev.html?load=file://MDsrv/example.ngl)
* [Documentation](http://arose.github.io/mdsrv/)


Features
--------

* Coordinate trajectories (animation, remote access)
* Trajectory formats supported (xtc/trr, nc/netcdf, dcd)
* [NGL Viewer](https://github.com/arose/ngl/) (Molecular structures, Density volumes, User interaction, Embeddable)
* Lightweight coordinate-only trajecotry reader (via [SimpleTraj](https://github.com/arose/simpletraj/)



Table of contents
=================

* [Documentation](#documentation)
* [RESTful API](#restful-api)
* [NGL browser support](#ngl browser-support)
* [Acknowledgments](#acknowledgments)
* [Cite](#cite)


Documentation
============

Detailed information concerning the installation, deployment and usage can be found at the [documentation](http://arose.github.io/mdsrv/).


Installation
============

From PyPI:

    pip install mdsrv


Running
=======

The `mdsrv` command starts a local server and opens a browser window with the web application.

To use a custom configuration file

    mdsrv --cfg my_conf.cfg


Load a topology and trajectory at startup

    mdsrv struc.gro traj.xtc


Configuration file
------------------

Optional. Copy/rename the sample [app.cfg](app.cfg.sample) file. It allows e.g. setting `data_dir` data directories that will be accessible through the web server and to define access restrictions.


Deployment
==========

The Apache Webserver can used to run the server via `mod_wsgi`. First make sure you have everything required installed:

    sudo apt-get install git apache2 libapache2-mod-wsgi


Then you need to create a wsgi configuration file to be referenced in the Apache configuration. There is an example named [mdsrv.wsgi.sample](mdsrv.wsgi.sample) in the root directory of this package. Also, a snippet showing how the configuration for Apache should look like can be found in the [apache.config.sample](apache.config.sample) file.

Finally, to restart apache issue

    sudo /etc/init.d/apache2 restart



RESTful API
===========

The RESTful API is the interface through which the web application gets all data but it may be also used to access the served trajectory data from other applications.


File content
------------

To retrieve a file from `data_dir` `<root>` with file path `<filename>` call:

    /file/<root>/<filename>


Directory content description
-----------------------------

To get a JSON description of available `data_dir` directories call:

    /dir/


To get a JSON description of the directory content in `data_dir` `<root>` call:

    /dir/<root>/


To get a JSON description of the directory content in `data_dir` `<root>` at path `<path>` call:

    /dir/<root>/<path>


The JSON description is a list of file or sub-directory entries:

```JSON
[
    {
        "name": "name of sub-directory",
        "path": "path relative to `<root>`",
        "dir": "`true` if entry is a directory",
        "restricted": "`true` if access is restricted"
    },
    {
        "name": "name of the file",
        "path": "path relative to `<root>`",
        "size": "file size in bytes"
    },
    {
        ...
    }
]
```


Frame count
-----------

To get the number of frames the trajectory in `data_dir` `<root>` with file path `<filename>` has call:

    /traj/numframes/<root>/<filename>


Frame coordinates
-----------------

To get the coordinates of frame number `<frame>` of the trajectory in `data_dir` `<root>` with file path `<filename>` call:

    /traj/frame/<frame>/<root>/<filename>


The set of atoms for which coordinates should be returned can be restricted by `POST`ing an `atomIndices` parameter with the following format. A list of index ranges is defined by pairs of integers separated by semi-colons (`;`) where the two integers within a pair are separated by a comma (`,`). To select atoms with indices (starting at zero) 5 to 10 and 22 to 30 send:

    5,10;22,30


The coordinate frame is returned in binary format and also contains the frame number, the simulation time (when available) and the box vectors.

| Offset | Size |  Type | Description                  |
| -----: | ---: | ----: | :--------------------------- |
|      0 |    4 |   int | frame number                 |
|      4 |    4 | float | simulation time              |
|      8 |    4 | float | X coordinate of box vector A |
|     12 |    4 | float | Y                            |
|     16 |    4 | float | Z                            |
|     20 |    4 | float | X coordinate of box vector B |
|     24 |    4 | float | Y                            |
|     28 |    4 | float | Z                            |
|     32 |    4 | float | X coordinate of box vector C |
|     36 |    4 | float | Y                            |
|     40 |    4 | float | Z                            |
|     44 |    4 | float | X coordinate of first atom   |
|     48 |    4 | float | Y                            |
|     52 |    4 | float | Z                            |
|    ... |  ... |   ... | ...                          |



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
* DFG Projekt HI 1502


Cite
====

When using MGsrv please cite:

* A. S. Rose, and MDsrv Contributors. MDsrv v0.2 Zenodo (2016), doi:10.5281/zenodo.45961.  [doi:10.5281/zenodo.45961](http://dx.doi.org/10.5281/zenodo.45961)
* AS Rose and PW Hildebrand. _NGL Viewer: a web application for molecular visualization._ Nucl Acids Res (1 July 2015) 43 (W1): W576-W579 first published online April 29, 2015. [doi:10.1093/nar/gkv402](https://doi.org/10.1093/nar/gkv402)
