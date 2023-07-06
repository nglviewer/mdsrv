#!/usr/bin/env python
import sys
from pathlib import Path
path_root = Path(__file__).parents[1]
sys.path.append(str(path_root) + "/mdsrv")
from trajectory import *
import pytest

# Adjust the below values to your desired file / file type for testing. 
# Note: use the relative path from the folder you are executing from for the file.
filename = "data/md.xtc"
TESTING_FILE = XtcTrajectory(filename, "")

def test_distance():
    atom0, atom1, frame = 93, 74, [0]
    assert str(round(TESTING_FILE.get_distance(atom0, atom1, frame)[0], 2)) == '3.83'

def test_angle():
    atom0, atom1, atom2, frame = 23, 74, 138, [10]
    assert str(round(TESTING_FILE.get_angle(atom0, atom1, atom2, frame)[0], 1)) == '143.4'

def test_dihedral():
     atom0, atom1, atom2, atom3, frame = 74, 23, 127, 145, [15]
     assert str(round((TESTING_FILE.get_dihedral(atom0, atom1, atom2, atom3, frame))[0], 1)) == '23.8'
