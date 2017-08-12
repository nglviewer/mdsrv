#!/usr/bin/env python
import sys
from mdsrv import trajectory


def main(argv):

    print('Importarray: ')
    print(trajectory.importarray)

    print('test for loading via gui:')
    print(trajectory.get_trajectory(argv[0], ''))
    print(trajectory.importarray)
    
    print('test for loading with command + struc&traj:')
    print(trajectory.get_trajectory(argv[0], argv[1]))
    print(trajectory.importarray)
    
    print('Extratest: Import mdtraj')
    try:
        import mdtraj
        print('success')
    except ImportError as e:
        print('error',e)

    print('Extratest: Import mdanalysis')
    try:
        import mdanalysis
        print('success')
    except ImportError as e:
        print('error',e)

    print('Extratest: mdtraj functionality')
    try:
        from mdtraj.formats import XTCTrajectoryFile
        xtc = XTCTrajectoryFile( argv[0], 'r' )
        xtc_traj = xtc.read(n_frames=1)
        print('success:', xtc_traj)
    except Exception as ex:
        template = "An exception of type {0} occurred. Arguments:\n{1!r}"
        message = template.format(type(ex).__name__, ex.args)
        print(message, ex)

if __name__ == "__main__":
    main(argv=sys.argv[1:])