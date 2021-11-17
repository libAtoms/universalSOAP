#!/usr/bin/env python

import sys

if len(sys.argv) < 2:
    sys.stderr.write("Usage: {} config.xyz [ config.xyz ... ]\n".format(sys.argv[0]))
    sys.exit(1)

import os
import ase.io
import traceback

from ase.optimize.precon import PreconLBFGS
from ase.constraints import UnitCellFilter
from utilities import at_neq, FixScaledAffine

import calculator

def relax(at, periodic):
    iter_n_steps = 10
    pre_relax_at = None

    print("    pre relax cell\n", at.get_cell())
    print("    pre relax pos\n",at.get_positions())
    do_again = True
    failed = False
    while do_again:
        calculator.cleanup()
        at.set_calculator(calculator.get(periodic))
        pre_relax_at = at.copy()
        if not periodic: # non periodic, relax w.r.t. positions once
            at_cell = at
        else: # periodic, relax w.r.t. cell only, repeatedly (to ensure self-consistent k point mesh and plane wave set)
            at_cell = UnitCellFilter(at, hydrostatic_strain=True)
        opt = PreconLBFGS(at_cell)
        try:
            opt.run(fmax=0.02, smax=0.005, steps=iter_n_steps)
        except RuntimeError:
            print("Failed, exception:")
            traceback.print_exc()
            if not failed: # try again, once
                print("RuntimeError in opt.run, trying again")
                failed = True
                continue # run another attempt
            # continue normally, which will stop if nothing as changed

        print("n_steps", opt.get_number_of_steps())
        # if it's not periodic and initial run converged (sufficiently few steps), break
        if not periodic and opt.get_number_of_steps() < iter_n_steps:
            do_again = False
        else:
            do_again = at_neq(pre_relax_at, at)

    calculator.cleanup()
    try:
        at.info["OUTPUT_moment"] = at.get_magnetic_moment()
    except:
        pass
    at.info["OUTPUT_energy"] = at.get_potential_energy()
    at.arrays["OUTPUT_forces"] = at.get_forces()
    at.info["OUTPUT_stress"] = at.get_stress()

    print("    post relax cell\n", at.get_cell())
    print("    post relax pos\n",at.get_positions())
    if "OUTPUT_moment" in at.info:
        print("    post relax moment",at.info["OUTPUT_moment"])
    print("    post relax energy",at.info["OUTPUT_energy"])
    print("    post relax forces\n",at.arrays["OUTPUT_forces"])
    print("    post relax stress\n",at.info["OUTPUT_stress"])

Zs = set()
for f in sys.argv[1:]:
    for at in ase.io.read(f,":"):
        Zs |= set(at.get_atomic_numbers())
Zs = list(Zs)
calculator.set_params(Zs)

for f in sys.argv[1:]:
    print("file",f)
    print("")

    ats=[]
    periodic = not "_nonperiodic" in f
    for at in ase.io.read(f,":"):

        print("do relaxation")
        if periodic: # relax cell only for periodic systems
            at.set_constraint(FixScaledAffine(list(range(len(at)))))
        relax(at, periodic)

        ats.append(at)

        print("")
        sys.stdout.flush()

    ase.io.write(os.path.join(os.path.dirname(f),"OUTPUT_"+os.path.basename(f)), ats)
