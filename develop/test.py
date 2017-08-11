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
    import mdtraj



if __name__ == "__main__":
    main(argv=sys.argv[1:])