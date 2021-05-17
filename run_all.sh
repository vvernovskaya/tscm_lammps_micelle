#!/bin/bash

echo "-- started executing the script"

mkdir process
cd process

temp=0
temp_step=0.15

for (( i=0; i < 11; ++i ))
do
mkdir temp_$temp

cd temp_$temp
cp /home/common/studtscm09/study/tscm_lammps_micelle/micelle/in.micelle_modif ./
sed  "s/ZZZtemp/$temp/g" in.micelle_modif > in.micelle_run
echo "-- -- replaced temperature parameter with $temp"

echo "-- -- started lammps simulation for $temp"
srun -N 1 --ntasks-per-node=8 -J lammps_vernovskaya --comment="Lammps micelle run" -p RT ~/bin/lmp_mpi -in in.micelle_run
echo "-- -- finished"

echo "-- -- running awk for $temp"
awk -f ../../awk_energy.sh log.micelle

echo "-- -- started making pickle from dump.micelle for $temp"
python3 ../../pickle_input_data.py
echo "-- -- finished"

echo "-- -- started calculating msd for $temp"
python3 ../../msd.py
echo "-- -- finished"

done
