#!/usr/bin/env python

import sys
if len(sys.argv) < 2:
    sys.stderr.write("Usage: {} Z [ Z ... ]\n".format(sys.argv[0]))
    sys.exit(1)

import matplotlib
matplotlib.use('PDF')
from matplotlib import pyplot as pp

import os, ase.data, glob, re, json, numpy as np
from universal_SOAPs import pair_bond_lengths, SOAP_hypers

length_scales = json.load(open("length_scales.json"))
for k in list(length_scales.keys()):
    if isinstance(k, str):
        length_scales[int(k)] = length_scales[k]

def plot_center(ax, ctr_bond_lengths, ctr_hypers, y, show_longest=True):
    ax.scatter([ctr_bond_lengths[0]], [y], c="red",    s=120.0, label="min bond len" if y == 0 else None)
    ax.scatter([ctr_bond_lengths[1]], [y], c="orange", s=120.0, label="self bond len" if y == 0 else None)
    if show_longest:
        ax.scatter([ctr_bond_lengths[2]], [y], c="limegreen",  s=60.0, marker="o", label="longest bond len" if y == 0 else None)

    for (r_cut_i, (r_cut, r_trans)) in enumerate([(h['cutoff'],h['cutoff_transition_width']) for h in ctr_hypers]):
        ax.plot([r_cut-r_trans,r_cut], [y]*2, marker=None, c="blue", label="SOAP cutoff" if r_cut_i == 0 and y == 0 else None)
        ax.scatter([r_cut-0.5*r_trans], [y], marker='D', s=8.0, c="blue", label=None)

Zs = [int(Z) for Z in sys.argv[1:]]

#elemental
ax = pp.figure().add_subplot(111)
y_labels = []
for (Zi, Z) in enumerate(sorted(set(Zs))):
    hypers = SOAP_hypers([Z], length_scales, 1.5, False, False)

    plot_center(ax, pair_bond_lengths(Z, [Z],length_scales), hypers[Z], Zi, False)

    y_labels.append("{0}-{0}".format(ase.data.chemical_symbols[Z]))

ax.set_xlabel("r ($\AA$)")
ax.set_xticks(range(12), minor=True)
ax.set_xticks(range(0,12,2))
ax.set_yticks(range(len(y_labels)+1))
ax.set_yticklabels(y_labels)
ax.set_ylabel("index")
if len(set(Zs)) == 2:
    ax.set_ylim(-0.2, len(y_labels)-0.2)
else:
    ax.set_ylim(-0.2, len(y_labels)-0.8)
ax.grid(True, axis='both')
ax.legend(bbox_to_anchor=(1,1))
pp.savefig("universal_SOAPs_elemental.pdf", bbox_inches='tight')

#binary
ax = pp.figure().add_subplot(111)
y_labels = []
ii = 0
for (pair_i, Z_pair) in enumerate(zip(Zs[0::2],Zs[1::2])):
    print("Z_pair",Z_pair)
    hypers = SOAP_hypers(Z_pair, length_scales, 1.5, False, False)
    for (Zctr_i, Zctr) in enumerate(Z_pair):
        plot_center(ax, pair_bond_lengths(Zctr, Z_pair, length_scales), hypers[Zctr], ii)
        y_labels.append("{0}-{1} : {2}".format( ase.data.chemical_symbols[Z_pair[0]], ase.data.chemical_symbols[Z_pair[1]], ase.data.chemical_symbols[Zctr] ))
        ii += 1

        self_hypers = SOAP_hypers([Zctr], length_scales, 1.5, False, False)
        plot_center(ax, pair_bond_lengths(Zctr, [Zctr]* 2, length_scales), self_hypers[Zctr], ii)
        y_labels.append("{0}-{1}".format( ase.data.chemical_symbols[Zctr], ase.data.chemical_symbols[Zctr]) )
        ii += 1

    ii += 1
    y_labels.append(None)

ax.set_xlabel("r ($\AA$)")
ax.set_xticks(range(12), minor=True)
ax.set_xticks(range(0,12,2))
ax.set_yticks(range(len(y_labels)+1))
ax.set_yticklabels(y_labels)
ax.set_ylabel("index")
ax.set_ylim(-0.2, len(y_labels)-0.8)
ax.grid(True, axis='both')
ax.legend(bbox_to_anchor=(1,1))
pp.savefig("universal_SOAPs_binary.pdf", bbox_inches='tight')

# #ternary
# for (triplet_i, Z_triplet) in enumerate([(37,22,8),(26,6,1),(14,8,1)]):
#     ax = pp.figure().add_subplot(111)
#     y_labels = []
#     ii = 0
#     for (Zctr_i, Zctr) in enumerate(Z_triplet):
#         grid_cutoff_data = SOAP_cutoff_grid(Zctr, Z_triplet, element_bond_lengths)
#         scale_center_cutoff_data = SOAP_cutoff_scale_center(Zctr, Z_triplet, element_bond_lengths)
#         plot_center(ax, grid_cutoff_data, scale_center_cutoff_data, ii)
#         ii += 1
#         y_labels.append("{0}-{1}-{2} : {3}".format( ase.data.chemical_symbols[Z_triplet[0]], ase.data.chemical_symbols[Z_triplet[1]], ase.data.chemical_symbols[Z_triplet[2]],
#             ase.data.chemical_symbols[Zctr] ))
# 
#         grid_cutoff_data = SOAP_cutoff_grid(Zctr, [Zctr], element_bond_lengths)
#         scale_center_cutoff_data = SOAP_cutoff_scale_center(Zctr, [Zctr], element_bond_lengths)
#         plot_center(ax, grid_cutoff_data, scale_center_cutoff_data, ii)
#         ii += 1
#         y_labels.append("{0}-{1}".format( ase.data.chemical_symbols[Zctr], ase.data.chemical_symbols[Zctr]) )
# 
#     ii += 1
#     y_labels.append(None)
# 
#     ax.set_xlabel("r ($\AA$)")
#     ax.set_xticks(range(18), minor=True)
#     ax.set_xticks(range(0,18,2))
#     ax.set_yticks(range(len(y_labels)+1))
#     ax.set_yticklabels(y_labels)
#     ax.set_ylabel("index")
#     ax.grid(True, axis='both')
#     ax.legend(bbox_to_anchor=(1,1))
#     pp.savefig("universal_SOAPs_ternary_{}_{}_{}.pdf".format(
#         ase.data.chemical_symbols[Z_triplet[0]],ase.data.chemical_symbols[Z_triplet[1]],ase.data.chemical_symbols[Z_triplet[2]]),
#         bbox_inches='tight')
