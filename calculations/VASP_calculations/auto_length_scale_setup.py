#!/usr/bin/env python

from __future__ import print_function

import sys, ase, ase.io, structure_scale, glob, numpy as np, ase.data, os
import argparse


p = argparse.ArgumentParser()
p.add_argument("-Z", type=int, help="atomic number", required=True)
p.add_argument("-factor", type=float, help="factor for initial length scale", default=1.0)
p.add_argument("-non_magnetic", action='store_true', help="do non magnetic calculation")
args = p.parse_args()

my_path=os.path.split(sys.argv[0])[0]

approx_b = ase.data.covalent_radii[args.Z]*2.0 * args.factor

def do_struct(name, struct, coord, fout, min_vacuum=None):
    at = ase.io.read(glob.glob(os.path.join(my_path,"AFLOW_structs/{}_*xyz".format(struct)))[0])
    at.info["structure_name"] = name
    at.set_atomic_numbers([args.Z] * len(at))
    if coord == 1:
        use_approx_b = approx_b
    else:
        use_approx_b = approx_b * ((float(coord)/3)  ** 0.25 )
    sys.stderr.write("{} {} {}\n".format(name, coord, use_approx_b))
    structure_scale.scale_shortest_bond([at], use_approx_b, min_vacuum=min_vacuum)
    if not args.non_magnetic:
        at.set_initial_magnetic_moments([1.0] + [0.0] * (len(at)-1))
        # # AFM
        # at.set_initial_magnetic_moments([(-1.0)**i for i in range(len(at))])
    ase.io.write(fout, at, format="extxyz")

with open("coordination_dependence_Z_{}_periodic.extxyz".format(args.Z),"w") as fout:
    for (name, struct, coord) in [("fcc", "A1",12),("bcc","A2",8),("beta-Sn","A5_alternative_setting",6),("diamond","A4",4)]:
        do_struct(name, struct, coord, fout)

with open("coordination_dependence_Z_{}_semiperiodic.extxyz".format(args.Z),"w") as fout:
    for (name, struct, coord) in [("AA-graphite","AA_graphite",3)]:
        do_struct(name, struct, coord, fout)

with open("coordination_dependence_Z_{}_nonperiodic.extxyz".format(args.Z),"w") as fout:
    for (name, struct, coord) in [("dimer","dimer",1)]:
        do_struct(name, struct, coord, fout, min_vacuum = 5.0)
