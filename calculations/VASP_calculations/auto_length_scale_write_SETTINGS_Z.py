#!/usr/bin/env python

from __future__ import print_function

import sys, argparse

parser = argparse.ArgumentParser(description="write SETTINGS_Z_*.py file from auto-length scale calculations")
parser.add_argument("--files", "-f", nargs='+', type=str, action='store', help='files with structures')
parser.add_argument("--use_for_volume", "-V", nargs='+', type=int, action='store', help='indices of files to use for volume')
parser.add_argument("--use_for_bond", "-b", nargs='+', type=int, action='store', help='indices of files to use for bond length')
parser.add_argument("--use_for_min_bond", "-m", nargs='+', type=int, action='store', help='indices of files to use for minimal bond length')
args = parser.parse_args()

import ase.io, numpy as np, structure_scale
from utilities import round_sigfigs

ats = []
for at_file in args.files:
    ats.append(ase.io.read(at_file,":"))

# find volume of lowest E structure
global_min_E = None
for file_ind in args.use_for_volume:
    Es = [ at.info["OUTPUT_energy"]/len(at) for at in ats[file_ind] ]
    min_E_ind = np.argmin(Es)
    if global_min_E is None or Es[min_E_ind] < global_min_E:
        global_min_E = Es[min_E_ind]
        at = ats[file_ind][min_E_ind]
        min_E_vol = at.get_volume()/len(at)
        min_E_vol_name = at.info["structure_name"]

global_min_E = None
for file_ind in args.use_for_bond:
    Es = [ at.info["OUTPUT_energy"]/len(at) for at in ats[file_ind] ]
    min_E_ind = np.argmin(Es)
    if global_min_E is None or Es[min_E_ind] < global_min_E:
        global_min_E = Es[min_E_ind]
        at = ats[file_ind][min_E_ind]
        min_E_b = structure_scale.shortest_bond(at)
        min_E_b_name = at.info["structure_name"]

shortest_b = None
for file_ind in args.use_for_min_bond:
    bs = [ structure_scale.shortest_bond(at) for at in ats[file_ind] ]
    min_b_ind = np.argmin(bs)
    if shortest_b is None or bs[min_b_ind] < shortest_b:
        shortest_b = bs[min_b_ind]
        shortest_b_name = ats[file_ind][min_b_ind].info["structure_name"]

sys.stderr.write("volume structure {} V {}\n".format(min_E_vol_name, min_E_vol))
sys.stderr.write("typical bond structure {} bond {}\n".format(min_E_b_name, min_E_b))
sys.stderr.write("shortest bond structure {} bond {}\n".format(shortest_b_name, shortest_b))

print("BOND_LEN={}".format(round_sigfigs(min_E_b,2)))
print("VOL_PER_ATOM={}".format(round_sigfigs(min_E_vol,2)))
print("MIN_BOND_LEN={}".format(round_sigfigs(shortest_b,2)))
