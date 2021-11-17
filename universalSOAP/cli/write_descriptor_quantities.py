def main():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--Zs", nargs="+", type=int, help="atomic numbers to calculate descriptors for", required=True)
    parser.add_argument("--spacing", type=float, help="spacing ratio between SOAPs", default=1.5)
    parser.add_argument("--no_extra_inner", action="store_true", help="never add extra inner cutoffs")
    parser.add_argument("--no_extra_outer", action="store_true", help="never add extra outer cutoffs")
    parser.add_argument("--sharpness", type=float, help="sharpness factor for atom_gaussian_width, scaled to heuristic for GAP", default=1.0)
    parser.add_argument("--length_scales_file", help="JSON file with length scales", default="length_scales.json")
    args = parser.parse_args()

    import sys, yaml
    from universalSOAP import SOAP_hypers

    length_scales = yaml.safe_load(open(args.length_scales_file))

    hypers = SOAP_hypers(args.Zs, length_scales, args.spacing, args.no_extra_inner, args.no_extra_outer)

    yaml.dump(hypers, sys.stdout)
    print("")
