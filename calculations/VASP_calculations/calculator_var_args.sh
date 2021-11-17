module unload compilers lapack quip ase python
module load compilers/gnu lapack/mkl python/3 ase quip vasp
module list

echo 0 > N

export VASP_COMMAND_GAMMA='(i=`cat N`; cp INCAR INCAR.$i; cp POSCAR POSCAR.$i; echo $(( $i + 1 )) > N; vasp.gamma_para; cp OUTCAR OUTCAR.$i)'
export VASP_COMMAND_KPTS='( i=`cat N`; cp INCAR INCAR.$i; cp POSCAR POSCAR.$i; echo $(( $i + 1 )) > N; vasp.para;       cp OUTCAR OUTCAR.$i)'
export VASP_NCORE=16
export VASP_KPAR=8

ln -s ../potpaw_PBE .
