#!/bin/bash

if [[ $# -lt 1 || $1 == "-h" || $1 == "--help" ]]; then
    echo "Usage: $0 Z [ auto_length_scale_setup args ] " 1>&2
    exit 1
fi

Z=$1; shift

mkdir -p run_auto_length_scale_Z_${Z}
cd run_auto_length_scale_Z_${Z}

../auto_length_scale_setup.py -Z $Z $*

cp ../job.auto_length_scale_relax_all.pbs .
if [ ! -f OUTPUT_coordination_dependence_Z_${Z}_periodic.extxyz ] || \
   [ ! -f OUTPUT_coordination_dependence_Z_${Z}_semiperiodic.extxyz ] || \
   [ ! -f OUTPUT_coordination_dependence_Z_${Z}_nonperiodic.extxyz ]; then
    echo qsub job.auto_length_scale_relax_all.pbs
    qsub job.auto_length_scale_relax_all.pbs

    while [ ! -f OUTPUT_coordination_dependence_Z_${Z}_periodic.extxyz ] || \
          [ ! -f OUTPUT_coordination_dependence_Z_${Z}_semiperiodic.extxyz ] || \
          [ ! -f OUTPUT_coordination_dependence_Z_${Z}_nonperiodic.extxyz ]; do
        sleep 10
    done
else
    echo "relaxation job appears complete"
fi


echo "../auto_length_scale_write_SETTINGS_Z.py -f OUTPUT_coordination_dependence_Z_${Z}_periodic.extxyz \
                                                  OUTPUT_coordination_dependence_Z_${Z}_semiperiodic.extxyz \
                                                  OUTPUT_coordination_dependence_Z_${Z}_nonperiodic.extxyz  \
                                         -V 0 -b 0 1 -m 0 1 2 > SETTINGS_Z_${Z}_auto_length_scale.py 2> auto_length_scale_analysis"
../auto_length_scale_write_SETTINGS_Z.py -f OUTPUT_coordination_dependence_Z_${Z}_periodic.extxyz \
                                            OUTPUT_coordination_dependence_Z_${Z}_semiperiodic.extxyz \
                                            OUTPUT_coordination_dependence_Z_${Z}_nonperiodic.extxyz  \
                                         -V 0 -b 0 1 -m 0 1 2 > SETTINGS_Z_${Z}_auto_length_scale.py 2> auto_length_scale_analysis

cd ..
ln -fs run_auto_length_scale_Z_${Z}/SETTINGS_Z_${Z}_auto_length_scale.py SETTINGS_Z_${Z}.py
