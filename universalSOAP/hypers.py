import sys

def pair_bond_lengths(Zctr, Zs, length_scales):
    # self bond for this center
    self_bond = length_scales[Zctr]["bond_len"][0]

    # shortest bond that this element can make in this composition
    shortest_bond = 0.5*(length_scales[Zctr]["min_bond_len"][0] + min([length_scales[Z]["min_bond_len"][0] for Z in Zs]))

    # longest bond that this center needs to account for
    longest_bond = 0.5*(length_scales[Zctr]["bond_len"][0] + max([length_scales[Z]["bond_len"][0] for Z in Zs]))

    return (shortest_bond, self_bond, longest_bond)

def descriptor_len_scales_for_center(Zctr, Zs, length_scales, spacing=1.5, no_extra_inner=False, no_extra_outer=False, verbose=False):
    if verbose:
        sys.stderr.write("Zctr {}\n".format(Zctr))

    (shortest_bond, self_bond, longest_bond) = pair_bond_lengths(Zctr, Zs, length_scales)
    # print(Zctr, Zs, "scale_center got bond lengths", shortest_bond, self_bond, longest_bond)

    # factor between shortest bond and shortest cutoff threshold
    factor_inner=1.3
    # factor between self-bond and outer of two guaranteed cutoffs
    factor_lenscale=factor_inner*spacing*1.01 # guarantee min two SOAPs
    # factor between longest bond and longest cutoff threshold
    factor_outer=1.3

    r_cut_mid = self_bond*factor_lenscale

    descriptor_len_scales = [r_cut_mid]
    if verbose:
        sys.stderr.write("initial descriptor_len_scales {}\n".format(len(descriptor_len_scales)))

    # go in in factors of spacing until inside inner threshold (not including anything inside)
    inner_threshold = shortest_bond*factor_inner  # used to be short_bond
    while True:
        r_cut_mid /= spacing
        if r_cut_mid < inner_threshold:
            if verbose:
                sys.stderr.write("inner length scale too small, leaving loop\n")
            break
        if verbose:
            sys.stderr.write("adding inner descriptor length scale {}\n".format(r_cut_mid))
        descriptor_len_scales.insert(0, r_cut_mid)
        if no_extra_inner: # only add one smaller SOAP
            break

    if verbose:
        sys.stderr.write("after steps in descriptor_len_scales {}\n".format(len(descriptor_len_scales)))

    if not no_extra_outer:
        outer_threshold = longest_bond*factor_outer
        if outer_threshold > self_bond*factor_lenscale*1.1: # might need to add more long range SOAPs
            r_cut_mid = descriptor_len_scales[-1]
            # go out in factors of spacing until outside inner threshold (including one thing outside)
            while True:
                r_cut_mid *= spacing
                if verbose:
                    sys.stderr.write("adding outer length scale {}\n".format(r_cut_mid))
                descriptor_len_scales.append(r_cut_mid)
                if r_cut_mid >= outer_threshold:
                    if verbose:
                        sys.stderr.write("outer length scale  too big, leaving loop\n")
                    break

        if verbose:
            sys.stderr.write("after steps out descriptor_len_scales {}\n".format(len(descriptor_len_scales)))

    if verbose:
        sys.stderr.write("returning descriptor_len_scales {}\n".format(len(descriptor_len_scales)))
    return descriptor_len_scales

# https://stackoverflow.com/questions/3410976/how-to-round-a-number-to-significant-figures-in-python
def round_sigfigs(v, n_sig_figs):
    return '{:g}'.format(float('{:.{p}g}'.format(v, p=n_sig_figs)))

def SOAP_hypers(Zs, length_scales, spacing, no_extra_inner, no_extra_outer, sharpness=1.0):
    for Z in Zs:
        if Z not in length_scales:
            raise RuntimeError("key Z {} not present in length_scales table {}".format(Z, list(length_scales.keys())))
    hypers = {}
    for Zcenter in Zs:
        hypers[Zcenter] = []
        for length_scale in descriptor_len_scales_for_center(Zcenter, Zs, length_scales, spacing=spacing, no_extra_inner=no_extra_inner, no_extra_outer=no_extra_outer):
            r_trans = min(2.0, length_scale/3.5)
            r_cut = length_scale + r_trans/2.0
            hypers[Zcenter].append( { 'cutoff' : float(round_sigfigs(r_cut,2)), 'cutoff_transition_width' : float(round_sigfigs(r_trans,2)), 'atom_gaussian_width' : float(round_sigfigs(r_cut/8.0/sharpness,2)) } )
    return hypers
