
MDSrv is a simple server that enables remote access to coordinate trajectories from molecular dynamics simulations.

Supported formats are:

* xtc/trr
* nc, netcdf
* dcd

Thanks to code from MDAnalysis (href="http://mdanalysis.googlecode.com) there is random access to xtc/trr trajectory files via indexing and seeking capabilities added to the libxdrfile2 library.


Installation
============

Flask
-----

The server is based on *Flask*, which can be installed through *pip*:

```bash
sudo pip install Flask
```


Trajectory reading
------------------

For the efficient access of trajectory files some libraries need to be installed. First, make sure you have the python development files installed, e.g.

```bash
sudo apt-get install python-dev python-numpy
```

Then install the NetCDF libraries

```bash
sudo apt-get install libhdf5-serial-dev libnetcdf-dev
sudo pip install netCDF4
```

In case you get "ValueError: did not find HDF5 headers" try:

```bash
sudo su
find / -name "libhdf5*.so*"
# use what the above 'find' suggests to set 'HDF5_DIR'
export HDF5_DIR=/usr/lib/i386-linux-gnu/hdf5/serial/
pip install netCDF4
```

Libraries for reading xtc/trr and dcd files are included and can be installed with

```bash
sh install.sh
```


Configuration files
-------------------

Copy/rename the sample `app.cfg` file. It allows e.g. setting data directories that will be accessible through the web server and to define access restrictions.

```bash
cp app.cfg.sample app.cfg
```


Running
=======

A local development server can be started with the python script

```bash
python serve.py
```

which will use the `app.cfg` configuration file or with

```bash
python serve.py my_conf.cfg
```

to use the `my_conf.cfg` configuration file.



Deployment
==========

The Apache Webserver can used to run the server via `mod_wsgi`. First make sure you have everything required installed:

```bash
sudo apt-get install git apache2 libapache2-mod-wsgi
```

Then you need to create a wsgi configuration file to be referenced in the apache configuration. There is an example named `ngl.wsgi.sample` in the root directory of this package. Also, a snippet showing how the configuration for apache should look like can be found in the `apache.config.sample` file.

Finally, to restart apache issue

```bash
sudo /etc/init.d/apache2 restart
```


License
=======

Generally GPL 2, see the LICENSE file for details.
