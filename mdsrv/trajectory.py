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

importarray = [ False, False, False ]#, False ]

try:
    import MDAnalysis
    importarray[1] = True
except ImportError:
    pass

try:
    import mdtraj as md
    from mdtraj.formats import *
    importarray[0] = True
    importarray[2] = True
except ImportError:
    pass

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


def get_trajectory( file_name, struc_path ):
    ext = os.path.splitext( file_name )[1].lower()
    types = {
        ".xtc": [ XtcTrajectory, MDAnalysisTrajectory, MDTrajTrajectory ],
        ".trr": [ TrrTrajectory, MDAnalysisTrajectory, MDTrajTrajectory ],
        ".netcdf": [ NetcdfTrajectory, MDAnalysisTrajectory, MDTrajTrajectory ],
        ".nc": [ NetcdfTrajectory, MDAnalysisTrajectory, MDTrajTrajectory ],
        ".dcd": [ DcdTrajectory, MDAnalysisTrajectory, DcdTrajectory ],
        ".gro": [ GroTrajectory, MDAnalysisTrajectory, GroTrajectory ], 
        ".pdb": [ None, MDAnalysisTrajectory, MDTrajTrajectory ],
        ".lammpstrj": [ LammpsTrajectory, None, LammpsTrajectory ],
        ".gz": [ None, MDAnalysisTrajectory, MDTrajTrajectory ],
        ".xyz": [ XyzTrajectory, MDAnalysisTrajectory, MDTrajTrajectory ],
        ".mdcrd": [ None, MDAnalysisTrajectory, MDTrajTrajectory ],
        ".binpos": [ BinposTrajectory, None, MDTrajTrajectory ],
        ".h5": [ Hdf5Trajectory, None, MDTrajTrajectory ],
        ".dtr": [ DtrTrajectory, None, DtrTrajectory ],
        ".arc": [ ArcTrajectory, None, ArcTrajectory ],
        ".tng": [ TngTrajectory, None, MDTrajTrajectory ],
        ".dms": [ None, MDAnalysisTrajectory, None ],
        ".crd": [ None, MDAnalysisTrajectory, None ],
        '.trj': [ None, MDAnalysisTrajectory, None ],
        '.trz': [ None, MDAnalysisTrajectory, None ],
        '.ent': [ None, MDAnalysisTrajectory, None ],
        '.ncdf': [ None, MDAnalysisTrajectory, None ],
    }
    if ext in types:
        if struc_path!="" and importarray[1]:
            importarray[0] = False
        for index, elem in enumerate(importarray):
            if elem & (types[ext][index] != None ):
                return types[ ext ][index]( file_name, struc_path )
    else:
        raise Exception( "extension '%s' not supported" % ext )


class TrajectoryCache( object ):
    def __init__( self ):
        self.cache = {}
        self.mtime = {}
        self.parts = {}

    def add( self, path, pathList, struc_path ):
        self.cache[ path ] = TrajectoryCollection( pathList, struc_path )
        # initial mtimes
        mtime = {}
        for partPath in pathList:
            mtime[ partPath ] = os.path.getmtime( partPath )
        self.mtime[ path ] = mtime
        # initial pathList
        self.parts[ path ] = pathList

    def get( self, path, struc_path ):
        stem = os.path.basename( path )
        if stem.startswith( "@" ):
            pathList = frozenset(
                get_xtc_parts( stem, os.path.dirname( path ) )
            )
        else:
            pathList = frozenset( [ path ] )
        if path not in self.cache:
            self.add( path, pathList, struc_path )
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
    def __init__( self, file_name, struc_name ):
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
    def __init__( self, parts, struc_path ):
        self.parts = []
        for file_name in sorted( parts ):
            self.parts.append( get_trajectory( file_name, struc_path ) )
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
    def __init__( self, file_name, struc_name ):
        self.file_name = file_name
        self.tng = TNGTrajectoryFile( self.file_name, 'r' )
        self.tng_traj = self.tng.read(n_frames=1)
        self.tng.seek(0, whence=2)

        self.numatoms = len(self.tng_traj[0][0])
        self.numframes = self.tng.tell()

        self.x = None
        self.box = np.zeros( ( 3, 3 ), dtype=np.float32 )
        self.time = 0.0

    def _get_frame( self, index ):
        self.tng.seek(index)
        xyz, time, boxlength = self.tng.read(n_frames=1)
        self.box[ 0, 0 ] = boxlength[ 0 ][ 0 ][ 0 ] * 10
        self.box[ 1, 1 ] = boxlength[ 0 ][ 1 ][ 1 ] * 10
        self.box[ 2, 2 ] = boxlength[ 0 ][ 2 ][ 2 ] * 10
        self.x = xyz[ 0 ] * 10
        self.time = time[ 0 ]
        return self.box, self.x, self.time

    def __del__( self ):
        try:
            self.tng.close()
        except:
            pass


class ArcTrajectory( Trajectory ):
    def __init__( self, file_name, struc_name ):
        self.file_name = file_name
        self.arc = ArcTrajectoryFile( self.file_name, 'r' )
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
        try:
            self.arc.close()
        except:
            pass


class DtrTrajectory( Trajectory ):
    def __init__( self, file_name, struc_name ):
        self.file_name = file_name
        self.dtr = DTRTrajectoryFile( self.file_name, 'r' )
        self.dtr_traj = self.dtr.read(n_frames=1)
        self.dtr.seek(0, whence=2)

        self.numatoms = len(self.dtr_traj[0][0])
        self.numframes = self.dtr.tell()

        self.x = None
        self.box = np.zeros( ( 3, 3 ), dtype=np.float32 )
        self.time = 0.0

    def _get_frame( self, index ):
        self.dtr.seek(index)
        xyz, times, boxlength, boxangles = self.dtr.read(n_frames=1)
        self.box[ 0, 0 ] = boxlength[ 0 ][ 0 ]
        self.box[ 1, 1 ] = boxlength[ 0 ][ 1 ]
        self.box[ 2, 2 ] = boxlength[ 0 ][ 2 ]
        self.x = xyz[ 0 ]
        self.time = times[ 0 ]
        return self.box, self.x, self.time

    def __del__( self ):
        try:
            self.dtr.close()
        except:
            pass


class Hdf5Trajectory( Trajectory ):
    def __init__( self, file_name, struc_name ):
        self.file_name = file_name
        self.hdf5 = HDF5TrajectoryFile( self.file_name, 'r' )
        self.hdf5_traj = self.hdf5.read(n_frames=1)
        self.hdf5.seek(0, whence=2)

        self.numatoms = len(self.hdf5_traj[0][0])
        self.numframes = self.hdf5.tell()

        self.x = None
        self.box = np.zeros( ( 3, 3 ), dtype=np.float32 )
        self.time = 0.0

    def _get_frame( self, index ):
        self.hdf5.seek(index)
        self.hdf5_traj = self.hdf5.read(n_frames=1)
        xyz = self.hdf5_traj.coordinates
        boxlength = self.hdf5_traj.cell_lengths
        cell_lengths = self.hdf5_traj.cell_angles
        time = self.hdf5_traj.time
        self.time = time[ 0 ]
        self.box[ 0, 0 ] = cell_lengths[ 0 ][ 0 ] * 10
        self.box[ 1, 1 ] = cell_lengths[ 0 ][ 1 ] * 10
        self.box[ 2, 2 ] = cell_lengths[ 0 ][ 2 ] * 10
        self.x = xyz[ 0 ] * 10
        return self.box, self.x, self.time

    def __del__( self ):
        try:
            self.hdf5.close()
        except:
            pass


class LammpsTrajectory( Trajectory ):
    def __init__( self, file_name, struc_name ):
        self.file_name = file_name
        self.lammps = LAMMPSTrajectoryFile( self.file_name, 'r' )
        self.lammps_traj = self.lammps.read(n_frames=1)
        looping(self.lammps, self.lammps_traj[0])

        self.numatoms = len(self.lammps_traj[0][0])
        self.numframes = self.lammps.tell()

        self.x = None
        self.box = np.zeros( ( 3, 3 ), dtype=np.float32 )
        self.time = 0.0

    def _get_frame( self, index ):
        self.lammps.seek(index)
        xyz, cell_lengths, boxangles = self.lammps.read(n_frames=1)
        self.box[ 0, 0 ] = cell_lengths[ 0 ][ 0 ]
        self.box[ 1, 1 ] = cell_lengths[ 0 ][ 1 ]
        self.box[ 2, 2 ] = cell_lengths[ 0 ][ 2 ]
        self.x = xyz[0]
        return self.box, self.x, self.time

    def __del__( self ):
        try:
            self.lammps.close()
        except:
            pass


class GroTrajectory( Trajectory ):
    def __init__( self, file_name, struc_name ):
        self.file_name = file_name
        self.gro = GroTrajectoryFile( self.file_name, 'r' )
        self.gro_traj = self.gro.read()
        self.numatoms = len(self.gro_traj[0][0])
        self.numframes = len(self.gro_traj[0])

        self.x = None
        self.box = np.zeros( ( 3, 3 ), dtype=np.float32 )
        self.time = 0.0

    def _get_frame( self, index ):
        xyz, time, unitcell = self.gro_traj
        self.box = unitcell[ index ] * 10
        self.x = xyz[ index ] * 10
        try:
            self.time = time[ index ]
        except:
            self.time = index
        return self.box, self.x, self.time

    def __del__( self ):
        try:
            self.gro.close()
        except:
            pass


class TrrTrajectory( Trajectory ):
    def __init__( self, file_name, struc_name ):
        self.file_name = file_name
        self.trr = TRRTrajectoryFile( self.file_name, 'r' )
        self.trr_traj = self.trr.read(n_frames=1)
        looping2(self.trr, self.trr_traj[0])

        self.numatoms = len(self.trr_traj[0][0])
        self.numframes = self.trr.tell()+1

        self.x = None
        self.box = np.zeros( ( 3, 3 ), dtype=np.float32 )
        self.time = 0.0

    def _get_frame( self, index ):
        self.trr.seek(index)
        xyz, time, step, box, lambd = self.trr.read(n_frames=1)
        self.box = box[ 0 ] * 10
        self.x = xyz[ 0 ] * 10
        self.time = time[ 0 ]
        return self.box, self.x, self.time

    def __del__( self ):
        try:
            self.trr.close()
        except:
            pass


def looping2(traj, r_traj):
    stepsizes = [100000, 50000, 10000, 5000, 1000, 500, 100, 10, 1]
    for index, stepsize in enumerate(stepsizes):
        r = r_traj
        while r.size!=0:
            try:
                traj.seek(stepsize, whence=1)
                r = traj.read(n_frames=1)[0]
                stepsize += stepsizes[index]
                stepsize -= 1
            except:
                traj.seek(-1, whence=1)
                break
        try:
            stepsize -=stepsizes[index]
            traj.seek(-stepsize, whence=1)
            r = traj.read(n_frames=1)[0]
        except: break


class XtcTrajectory( Trajectory ):
    def __init__( self, file_name, struc_name ):
        self.file_name = file_name
        self.xtc = XTCTrajectoryFile( self.file_name, 'r' )
        self.xtc_traj = self.xtc.read(n_frames=1)
        looping2(self.xtc, self.xtc_traj[0])

        self.numatoms = len(self.xtc_traj[0][0])
        self.numframes = self.xtc.tell()

        self.x = None
        self.box = np.zeros( ( 3, 3 ), dtype=np.float32 )
        self.time = 0.0

    def _get_frame( self, index ):
        self.xtc.seek(index)
        xyz, time, step, box = self.xtc.read(n_frames=1)
        self.box = box[0] * 10
        self.x = xyz[0] * 10
        self.time = time[0]
        return self.box, self.x, self.time

    def __del__( self ):
        try:
            self.xtc.close()
        except:
            pass


class NetcdfTrajectory( Trajectory ):
    def __init__( self, file_name, struc_name ):
        # http://ambermd.org/netcdf/nctraj.pdf
        self.file_name = file_name
        self.netcdf = NetCDFTrajectoryFile( self.file_name )
        self.numatoms = self.netcdf.n_atoms
        self.numframes = self.netcdf.n_frames

        self.x = None
        self.box = np.zeros( ( 3, 3 ), dtype=np.float32 )
        self.time = 0.0

    def _get_frame( self, index ):
        self.netcdf.seek(index)
        xyz, time, cell_lengths, boxangles = self.netcdf.read(n_frames=1)
        try:
            self.box[ 0, 0 ] = cell_lengths[ 0 ][ 0 ]
            self.box[ 1, 1 ] = cell_lengths[ 0 ][ 1 ]
            self.box[ 2, 2 ] = cell_lengths[ 0 ][ 2 ]
        except: pass
        self.x = xyz[0]
        try:
            self.time = time[0]
        except:
            self.time = index
        return self.box, self.x, self.time

    def __del__( self ):
        try:
            self.netcdf.close()
        except:
            pass


def looping(traj, r_traj):
    stepsizes = [100000, 50000, 10000, 5000, 1000, 500, 100, 10, 1]
    for index, stepsize in enumerate(stepsizes):
        r = r_traj
        while r.size!=0:
            try:
                traj.seek(stepsize, whence=1)
                r = traj.read(n_frames=1)[0]
                stepsize += stepsizes[index]
            except: break
        try:
            stepsize -=stepsizes[index]
            traj.seek(-stepsize, whence=1)
            r = traj.read(n_frames=1)[0]
        except: break
        

class DcdTrajectory( Trajectory ):
    def __init__( self, file_name, struc_name ):
        self.file_name = file_name
        self.dcd = DCDTrajectoryFile( self.file_name, 'r' )
        self.dcd_traj = self.dcd.read(n_frames=1)
        looping(self.dcd, self.dcd_traj[0])
        
        self.numatoms = len(self.dcd_traj[0][0])
        self.numframes = self.dcd.tell()-2

        self.x = None
        self.box = np.zeros( ( 3, 3 ), dtype=np.float32 )
        self.time = 0.0

    def _get_frame( self, index ):
        self.dcd.seek(index)
        xyz, cell_lengths, boxangles = self.dcd.read(n_frames=1)
        try:
            self.box[ 0, 0 ] = cell_lengths[ 0 ][ 0 ]
            self.box[ 1, 1 ] = cell_lengths[ 0 ][ 1 ]
            self.box[ 2, 2 ] = cell_lengths[ 0 ][ 2 ]
        except: pass
        self.x = xyz[ 0 ]
        return self.box, self.x, self.time

    def __del__( self ):
        try:
            self.dcd.close()
        except:
            pass


class MdcrdTrajectory( Trajectory ):
    def __init__( self, file_name, struc_name ):
        self.file_name = file_name
        self.struc_name = struc_name
        topology = md.load( self.struc_name ).topology
        self.numatoms = topology.n_atoms
        self.mdcrd = MDCRDTrajectoryFile( self.file_name, self.numatoms )
        self.mdcrd_traj = self.mdcrd.read()
        self.numframes = len(self.mdcrd_traj[0])
        self.x = None
        self.box = np.zeros( ( 3, 3 ), dtype=np.float32 )
        self.time = 0.0

    def _get_frame( self, index ):
        xyz, cell_lengths = self.mdcrd_traj
        try:
            self.box[ 0, 0 ] = cell_lengths[ index ][ 0 ]
            self.box[ 1, 1 ] = cell_lengths[ index ][ 1 ]
            self.box[ 2, 2 ] = cell_lengths[ index ][ 2 ]
        except: pass
        self.x = xyz[ index ]
        return self.box, self.x, self.time

    def __del__( self ):
        try:
            self.mdcrd.close()
        except:
            pass


class BinposTrajectory( Trajectory ):
    def __init__( self, file_name, struc_name ):
        self.file_name = file_name
        self.binpos = BINPOSTrajectoryFile( self.file_name, 'r' )
        self.binpos_traj = self.binpos.read(n_frames=1)
        self.binpos.seek(-1, whence=2)

        self.numatoms = len(self.binpos_traj[0][0])
        self.numframes = self.binpos.tell()

        self.x = None
        self.box = np.zeros( ( 3, 3 ), dtype=np.float32 )
        self.time = 0.0

    def _get_frame( self, index ):
        self.binpos.seek(index)
        xyz = self.binpos.read(n_frames=1)
        self.x = xyz[0]
        return self.box, self.x, self.time

    def __del__( self ):
        try:
            self.binpos.close()
        except:
            pass


class XyzTrajectory( Trajectory ):
    def __init__( self, file_name, struc_name ):
        self.file_name = file_name
        self.xyz = XYZTrajectoryFile( self.file_name, 'r' )
        self.xyz_traj = self.xyz.read(n_frames=1)
        looping(self.xyz, self.xyz_traj)

        self.numframes = self.xyz.tell()
        self.numatoms = len(self.xyz_traj[0][0])

        self.x = None
        self.box = np.zeros( ( 3, 3 ), dtype=np.float32 )
        self.time = 0.0

    def _get_frame( self, index ):
        self.xyz.seek(index)
        xyz = self.xyz.read(n_frames=1)
        self.x = xyz[0]
        return self.box, self.x, self.time

    def __del__( self ):
        try:
            self.xyz.close()
        except:
            pass


class MDTrajTrajectory( Trajectory ):
    def __init__( self, file_name, struc_path ):
        self.file_name = file_name
        self.struc_name = struc_path
        filesize = os.path.getsize(self.file_name)
        if filesize <= 1500000000:
            self.frame =  md.load(self.file_name, top=self.struc_name)
            self.numframes = self.frame.n_frames
            self.numatoms = self.frame.n_atoms
        else:
            first_frame = md.load_frame(self.file_name, 0, self.struc_name)
            times = 0
            for chunk in md.iterload(self.file_name, top=self.struc_name, chunk=100, atom_indices=[1]):
                times += chunk.n_frames
            self.numframes = times
            self.numatoms = first_frame.n_atoms
            self.frame = None
        self.x = None
        self.box = np.zeros( ( 3, 3 ), dtype=np.float32 )
        self.time = 0.0

    def _get_frame( self, index ):
        if self.frame:
            frame = self.frame[index]
        else:
            frame = md.load_frame(self.file_name, index, self.struc_name)
        try:
            self.box = frame.unitcell_vectors * 10
        except:
            self.box = np.zeros( ( 3, 3 ), dtype=np.float32 )
            pass
        self.x = frame.xyz * 10
        self.time = frame.time
        return self.box, self.x, self.time


class MDAnalysisTrajectory( Trajectory ):
    def __init__( self, file_name, struc_path ):
        self.file_name = file_name
        self.struc_name = struc_path
        self.universe = MDAnalysis.Universe(self.struc_name, self.file_name)
        self.numatoms = self.universe.trajectory.n_atoms
        self.numframes = self.universe.trajectory.n_frames
        self.x = None
        self.box = np.zeros( ( 3, 3 ), dtype=np.float32 )
        self.time = 0.0

    def _get_frame( self, index ):
        frame = self.universe.trajectory[index]
        try:
            self.box[ 0, 0 ] = frame.dimensions[ 0 ]
            self.box[ 1, 1 ] = frame.dimensions[ 1 ]
            self.box[ 2, 2 ] = frame.dimensions[ 2 ]
        except:
            self.box = np.zeros( ( 3, 3 ), dtype=np.float32 )
            pass
        self.x = frame.positions
        self.time = frame.frame
        return self.box, self.x, self.time
