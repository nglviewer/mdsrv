# Change Log
All notable changes to this project will be documented in this file, following the suggestions of [Keep a CHANGELOG](http://keepachangelog.com/). This project adheres to [Semantic Versioning](http://semver.org/).


## [v0.3.5] - 2017-08-13
### Added
- WINDOWS support (tested for conda)
### Changed
- trajectory support switched from simpletraj to MDTraj with MDAnalysis as extra requirement
- NGL update to version 0.10.5-18 including bugfixes related to superpositioning, updated remove trajectory formats, IE11 workaround


## [v0.3.4] - 2017-07-31
### Added
- conda support via ngl channel
- delta time and time offset as CMD variables


## [v0.3.3] - 2017-07-27
### Changed
- NGL update to version 0.10.5-15 incl. bugfixes related to interpolation, change superpositioning on initial frame, add bounce direction for trajectoy player, animations
- script examples according to new NGL version
### Added
- conda support
- netcdf, gro, lammpstrj, hdf5, dtr, arc tng trajectory support from mdtraj


## [v0.3.2] - 2017-07-03
### Changed
- ngl update to version 0.10.5-2 incl. prmtop parser, traj time (delta time) settings, debug


## [v0.3.1] - 2017-07-02
### Changed
- major ngl update to version 0.10.5-1 incl. psf, netcdf, xtc (speedup), movable gui, ...


## [v0.3] - 2016-01-11
### Added
- --script arguments
- versioneer
- DOC: installation & deployment, usage, scripting

### Changed
- major ngl update to version 0.10.0-dev5


## [v0.2] - 2016-02-12
### Added
- --host and --port arguments
- DOC: described arguments of the comand line tool
[![DOI](https://zenodo.org/badge/doi/10.5281/zenodo.45961.svg)](http://dx.doi.org/10.5281/zenodo.45961)


## [v0.1.1] - 2016-01-02
### Added
- Initial release
[![DOI](https://zenodo.org/badge/doi/10.5281/zenodo.44286.svg)](http://dx.doi.org/10.5281/zenodo.44286)
