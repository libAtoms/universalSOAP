# universal-soap
scripts to create SOAP descriptors for arbitrary elements and combinations

Heuristics:
  * Length scales
    * Atomic (inputs)
      * typical bond length (from equilibrium bond length in lowest energy 2D or 3D structure)
      * minimal bond length (from shortest bond length of any equilibrium structure, including dimer)
    * Pairs: typical and minimal length scales equal to the arithmetic mean of the two corresponding atomic length scales
  * For each atomic number Z there is a set of length scales associated with it as the center, applying to all neighbor types
    * Typical Z-Z (homonuclear) bond length * 1.3
    * Add one spacing factor (currently 1.5) larger
    * Add additional shorter length scales, by factors of 1/spacing^n, as long as they are at least 1.3 times larger than shortest bond (over all Z\_center-Z2 pairs)
    * If the longest bond times 1.3 is more than 1.1 times larger than the outermost length scale so far, add additional longer length scales, by factors of spacing^n, until the longest one is larger than 1.3 times longest bond (over all Z\_center-Z2 pairs)
    * For each of these length scales there is an associated SOAP
      * The center of the cutoff transition, i,.e. `cutoff - 0.5 transition`, is equal to the length scale
      * The transition width is `min(0.25 length_scale, 2 Angstrom)`
      * The atom sigma is the `length_scale / 8`, divided by an optional `sharpness` factor

Files:

  * length\_scales.json: file with information on atomic length scales: minimum bond length, typical bond length, volume/atom.  For each of these values there's also a string for information source (e.g. URL), and dict of other info/links

  * universal\_SOAPs.py: routines that actually compute length scales and corresponding SOAP hyper-params
    * `descriptor_len_scales_for_center()` - length scales for a given species as center in the presences of any number of neighbor species
    * `SOAP_hypers()` - returns dict of SOAP hyperparams (`cutoff`, `cutoff_transition_width` and `atom_gaussian_width`) with element atomic numbers as keys, and list of 3 entry dicts as values, one dict per SOAP descriptor/length scale

  * write\_descriptor\_quantity\_json: Executable that reads length\_scales.json file and list of atomic numbers, and outputs json with per-descriptor `cutoff`, `transition`, and `atom_gaussian_width` values

## Example

The command `python write_descriptor_quantity_json --Zs 5 32` will return length scales needed to define the SOAP descriptors for a system with boron (5) and germanium (32). The output is

```
{"5": [{"cutoff": 2.6, "cutoff_transition_width": 0.64, "atom_gaussian_width": 0.32}, {"cutoff": 3.8, "cutoff_transition_width": 0.96, "atom_gaussian_width": 0.48}], "32": [{"cutoff": 3.8, "cutoff_transition_width": 0.94, "atom_gaussian_width": 0.47}, {"cutoff": 5.6, "cutoff_transition_width": 1.4, "atom_gaussian_width": 0.7}]}
```

So three SOAPs each the boron-centered and the germanium-centered descriptors, with cutoffs, cutoff_transition_widths and atom_gaussian_widths parameters given. 

