# cython: c_string_type=str, c_string_encoding=ascii
from __future__ import absolute_import
from __future__ import print_function

import os
import re
import sys
import array
import collections
import numpy as np
import warnings

from mdtraj.formats import *
from simpletraj import trajectory as simpletraj_trajectory

try:
    import cPickle as pickle
except ImportError:
    import pickle

if sys.version_info > (3,):
    long = int


def get_xtc_parts( name, directory ):
    pattern = re.escape( name[1:-4] ) + "\.part[0-9]{4,4}\.(xtc|trr)$"
    parts = []
    for f in os.listdir( directory ):
        m = re.match( pattern, f )
        if m and os.path.isfile( os.path.join( directory, f ) ):
            parts.append( os.path.join( directory, f ) )
    return sorted( parts )


def get_split_xtc( directory ):
    pattern = "(.*)\.part[0-9]{4,4}\.(xtc|trr)$"
    split = collections.defaultdict( int )
    for f in os.listdir( directory ):
        m = re.match( pattern, f )
        if( m ):
            split[ "@" + m.group(1) + "." + m.group(2) ] += 1
    if sys.version_info > (3,):
        return sorted( [ k for k, v in split.items() if v > 1 ] )
    else:
        return sorted( [ k for k, v in split.iteritems() if v > 1 ] )


def get_trajectory( file_name ):
    ext = os.path.splitext( file_name )[1].lower()
    types = {
        ".xtc": simpletraj_trajectory.XtcTrajectory,
        ".trr": simpletraj_trajectory.TrrTrajectory,
        ".netcdf": NetcdfTrajectory,
        ".nc": NetcdfTrajectory,
        ".dcd": simpletraj_trajectory.DcdTrajectory,
        ".gro": GroTrajectory,
        ".lammpstrj": LammpsTrajectory,
        ".h5": Hdf5Trajectory,
        ".dtr": DtrTrajectory,
        ".arc": ArcTrajectory,
        ".tng": TngTrajectory,
    }
    if ext in types:
        return types[ ext ]( file_name )
    else:
        raise Exception( "extension '%s' not supported" % ext )


class TrajectoryCache( object ):
    def __init__( self ):
        self.cache = {}
        self.mtime = {}
        self.parts = {}

    def add( self, path, pathList ):
        self.cache[ path ] = TrajectoryCollection( pathList )
        # initial mtimes
        mtime = {}
        for partPath in pathList:
            mtime[ partPath ] = os.path.getmtime( partPath )
        self.mtime[ path ] = mtime
        # initial pathList
        self.parts[ path ] = pathList

    def get( self, path ):
        stem = os.path.basename( path )
        if stem.startswith( "@" ):
            pathList = frozenset(
                get_xtc_parts( stem, os.path.dirname( path ) )
            )
        else:
            pathList = frozenset( [ path ] )
        if path not in self.cache:
            self.add( path, pathList )
        elif pathList != self.parts[ path ]:
            # print( "pathList changed, rebuilding" )
            del self.cache[ path ]
            self.add( path, pathList )
        else:
            updateRequired = False
            mtime = self.mtime[ path ]
            for partPath in pathList:
                if mtime[ partPath ] < os.path.getmtime( partPath ):
                    updateRequired = True
            if updateRequired:
                # print( "file modified, updating" )
                self.cache[ path ].update( True )
        return self.cache[ path ]


class Trajectory( object ):
    def __init__( self, file_name ):
        pass

    def update( self, force=False ):
        pass

    def _get_frame( self, index ):
        # return box, coords, time
        # box, coords in angstrom
        # time in ???
        pass

    def get_frame( self, index, atom_indices=None ):
        box, coords, time = self._get_frame( int( index ) )
        if atom_indices:
            coords = np.concatenate([
                coords[ i:j ].ravel() for i, j in atom_indices
            ])
        return {
            "numframes": self.numframes,
            "time": time,
            "box": box,
            "coords": coords
        }

    def get_frame_string( self, index, atom_indices=None ):
        frame = self.get_frame( index, atom_indices=atom_indices )
        return (
            array.array( "i", [ frame[ "numframes" ] ] ).tostring() +
            array.array( "f", [ frame[ "time" ] ] ).tostring() +
            array.array( "f", frame[ "box" ].flatten() ).tostring() +
            array.array( "f", frame[ "coords" ].flatten() ).tostring()
        )

    def get_path( self, atom_index, frame_indices=None ):
        if( frame_indices ):
            size = len( frame_indices )
            frames = map( int, frame_indices )
        else:
            size = self.numframes
            frames = range( size )
        path = np.zeros( ( size, 3 ), dtype=np.float32 )
        for i in frames:
            box, coords, time = self._get_frame( i )
            path[ i ] = coords[ atom_index ]
        return path

    def get_path_string( self, atom_index, frame_indices=None ):
        path = self.get_path( atom_index, frame_indices=frame_indices )
        return array.array( "f", path.flatten() ).tostring()

    def __del__( self ):
        pass


class TrajectoryCollection( Trajectory ):
    def __init__( self, parts ):
        self.parts = []
        for file_name in sorted( parts ):
            self.parts.append( get_trajectory( file_name ) )
        self.box = self.parts[ 0 ].box
        self._update_numframes()

    def _update_numframes( self ):
        self.numframes = 0
        for trajectory in self.parts:
            self.numframes += trajectory.numframes

    def update( self, force=False ):
        for trajectory in self.parts:
            trajectory.update( force=force )
        self._update_numframes()

    def _get_frame( self, index ):
        i = 0
        for trajectory in self.parts:
            if index < i + trajectory.numframes:
                break
            i += trajectory.numframes
        return trajectory._get_frame( index - i )

    def __del__( self ):
        for trajectory in self.parts:
            trajectory.__del__()


class TngTrajectory( Trajectory ):
    def __init__( self, file_name ):
        self.file_name = file_name
        self.tng = TNGTrajectoryFile( self.file_name )
        self.tng_traj = self.tng.read()
        self.numatoms = len(self.tng_traj[0][0])
        self.numframes = len(self.tng_traj[0])

        self.x = None
        self.box = np.zeros( ( 3, 3 ), dtype=np.float32 )
        self.time = 0.0

    def _get_frame( self, index ):
        xyz, time, boxlength = self.tng_traj
        self.box[ 0, 0 ] = boxlength[ index ][ 0 ][ 0 ] * 10
        self.box[ 1, 1 ] = boxlength[ index ][ 1 ][ 1 ] * 10
        self.box[ 2, 2 ] = boxlength[ index ][ 2 ][ 2 ] * 10
        self.x = xyz[ index ] * 10
        self.time = time[ index ]
        return self.box, self.x, self.time

    def __del__( self ):
        if self.tng:
            self.tng.close()


class ArcTrajectory( Trajectory ):
    def __init__( self, file_name ):
        self.file_name = file_name
        self.arc = ArcTrajectoryFile( self.file_name )
        self.arc_traj = self.arc.read()
        self.numatoms = len(self.arc_traj[0][0])
        self.numframes = len(self.arc_traj[0])

        self.x = None
        self.box = np.zeros( ( 3, 3 ), dtype=np.float32 )
        self.time = 0.0

    def _get_frame( self, index ):
        xyz, boxlength, boxangles = self.arc_traj
        try:
            self.box[ 0, 0 ] = boxlength[ index ][ 0 ]
            self.box[ 1, 1 ] = boxlength[ index ][ 1 ]
            self.box[ 2, 2 ] = boxlength[ index ][ 2 ]
        except: pass
        self.x = xyz[ index ]
        return self.box, self.x, self.time

    def __del__( self ):
        if self.arc:
            self.arc.close()


class DtrTrajectory( Trajectory ):
    def __init__( self, file_name ):
        self.file_name = file_name
        self.dtr = DTRTrajectoryFile( self.file_name )
        self.dtr_traj = self.dtr.read()
        self.numatoms = len(self.dtr_traj[0][0])
        self.numframes = len(self.dtr_traj[0])

        self.x = None
        self.box = np.zeros( ( 3, 3 ), dtype=np.float32 )
        self.time = 0.0

    def _get_frame( self, index ):
        xyz, times, boxlength, boxangles = self.dtr_traj
        self.box[ 0, 0 ] = boxlength[ index ][ 0 ]
        self.box[ 1, 1 ] = boxlength[ index ][ 1 ]
        self.box[ 2, 2 ] = boxlength[ index ][ 2 ]
        self.x = xyz[ index ]
        self.time = times[ index ]
        return self.box, self.x, self.time

    def __del__( self ):
        if self.dtr:
            self.dtr.close()


class Hdf5Trajectory( Trajectory ):
    def __init__( self, file_name ):
        self.file_name = file_name
        self.hdf5 = HDF5TrajectoryFile( self.file_name )
        self.hdf5_traj = self.hdf5.read()
        self.numatoms = len(self.hdf5_traj[0][0])
        self.numframes = len(self.hdf5_traj[0])

        self.x = None
        self.box = np.zeros( ( 3, 3 ), dtype=np.float32 )
        self.time = 0.0

    def _get_frame( self, index ):
        xyz = self.hdf5_traj.coordinates
        boxlength = self.hdf5_traj.cell_lengths
        cell_lengths = self.hdf5_traj.cell_angles
        time = self.hdf5_traj.time
        self.time = time[ index ]
        self.box[ 0, 0 ] = cell_lengths[ index ][ 0 ] * 10
        self.box[ 1, 1 ] = cell_lengths[ index ][ 1 ] * 10
        self.box[ 2, 2 ] = cell_lengths[ index ][ 2 ] * 10
        self.x = xyz[ index ] * 10
        return self.box, self.x, self.time

    def __del__( self ):
        if self.hdf5:
            self.hdf5.close()


class LammpsTrajectory( Trajectory ):
    def __init__( self, file_name ):
        self.file_name = file_name
        self.lammps = LAMMPSTrajectoryFile( self.file_name )
        self.lammps_traj = self.lammps.read()
        self.numatoms = len(self.lammps_traj[0][0])
        self.numframes = len(self.lammps_traj[0])

        self.x = None
        self.box = np.zeros( ( 3, 3 ), dtype=np.float32 )
        self.time = 0.0

    def _get_frame( self, index ):
        xyz, boxlength, boxangles = self.lammps_traj
        cell_lengths = boxlength
        self.box[ 0, 0 ] = cell_lengths[ index ][ 0 ]
        self.box[ 1, 1 ] = cell_lengths[ index ][ 1 ]
        self.box[ 2, 2 ] = cell_lengths[ index ][ 2 ]
        self.x = xyz[index]
        return self.box, self.x, self.time

    def __del__( self ):
        if self.lammps:
            self.lammps.close()


class GroTrajectory( Trajectory ):
    def __init__( self, file_name ):
        self.file_name = file_name
        with GroTrajectoryFile( self.file_name, 'r' ) as fp:
            self.gro = fp.read()
        self.numatoms = len(self.gro[0][0])
        self.numframes = len(self.gro[0])

        self.x = None
        self.box = np.zeros( ( 3, 3 ), dtype=np.float32 )
        self.time = 0.0

    def _get_frame( self, index ):
        xyz, time, unitcell = self.gro
        self.box = unitcell[ index ] * 10
        self.x = xyz[ index ] * 10
        try:
            self.time = time[ index ]
        except:
            self.time = index
        return self.box, self.x, self.time

    def __del__( self ):
        if self.gro:
            del self.gro


class TrrTrajectory( Trajectory ):
    def __init__( self, file_name ):
        self.file_name = file_name
        with TRRTrajectoryFile( self.file_name, 'r' ) as fp:
            self.trr = fp.read()
        self.numatoms = len(self.trr[0][0])
        self.numframes = len(self.trr[1])

        self.x = None
        self.box = np.zeros( ( 3, 3 ), dtype=np.float32 )
        self.time = 0.0

    def _get_frame( self, index ):
        xyz, time, step, box, lambd = self.trr
        self.box = box[ index ] * 10
        self.x = xyz[ index ] * 10
        self.time = time[ index ]
        return self.box, self.x, self.time

    def __del__( self ):
        if self.trr:
            del self.trr


class XtcTrajectory( Trajectory ):
    def __init__( self, file_name ):
        self.file_name = file_name
        with XTCTrajectoryFile( self.file_name, 'r' ) as fp:
            self.xtc = fp.read()
        self.numatoms = len(self.xtc[0][0])
        self.numframes = len(self.xtc[1])

        self.x = None
        self.box = np.zeros( ( 3, 3 ), dtype=np.float32 )
        self.time = 0.0

    def _get_frame( self, index ):
        xyz, time, step, box = self.xtc
        self.box = box[ index ] * 10
        self.x = xyz[ index ] * 10
        self.time = time[ index ]
        return self.box, self.x, self.time

    def __del__( self ):
        if self.xtc:
            del self.xtc


class NetcdfTrajectory( Trajectory ):
    def __init__( self, file_name ):
        # http://ambermd.org/netcdf/nctraj.pdf
        self.file_name = file_name
        self.netcdf = NetCDFTrajectoryFile( self.file_name )
        self.numatoms = self.netcdf.n_atoms
        self.numframes = self.netcdf.n_frames
        self.netcdf_traj = self.netcdf.read()

        self.x = None
        self.box = np.zeros( ( 3, 3 ), dtype=np.float32 )
        self.time = 0.0

    def _get_frame( self, index ):
        xyz, time, boxlength, boxangles = self.netcdf_traj
        cell_lengths = boxlength
        try:
            self.box[ 0, 0 ] = cell_lengths[ index ][ 0 ]
            self.box[ 1, 1 ] = cell_lengths[ index ][ 1 ]
            self.box[ 2, 2 ] = cell_lengths[ index ][ 2 ]
        except: pass
        self.x = xyz[index]
        self.time = time[index]
        return self.box, self.x, self.time

    def __del__( self ):
        if self.netcdf:
            self.netcdf.close()


class DcdTrajectory( Trajectory ):
    def __init__( self, file_name ):
        self.file_name = file_name
        self.dcd = DCDTrajectoryFile( self.file_name )
        self.dcd_traj = self.dcd.read()
        self.numatoms = len(self.dcd_traj[0][0])
        self.numframes = len(self.dcd_traj[0])
        self.x = None
        self.box = np.zeros( ( 3, 3 ), dtype=np.float32 )
        self.time = 0.0

    def _get_frame( self, index ):
        xyz, boxlength, boxangles = self.dcd_traj
        cell_lengths = boxlength
        try:
            self.box[ 0, 0 ] = cell_lengths[ index ][ 0 ]
            self.box[ 1, 1 ] = cell_lengths[ index ][ 1 ]
            self.box[ 2, 2 ] = cell_lengths[ index ][ 2 ]
        except: pass
        self.x = xyz[ index ]
        return self.box, self.x, self.time

    def __del__( self ):
        if self.dcd:
            self.dcd.close()