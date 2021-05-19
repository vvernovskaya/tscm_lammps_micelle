#!/bin/bash

num_params=5

echo "-- started executing the script"

mkdir process
cd process

temp=0
temp_step=0.15

cp /home/common/studtscm09/study/tscm_lammps_micelle/micelle/in.micelle_modif ./
cp /home/common/studtscm09/study/tscm_lammps_micelle/micelle/data.micelle ./
cp /home/common/studtscm09/study/tscm_lammps_micelle/micelle/def.micelle ./

for (( i=0; i < $num_params; ++i ))
do

sed  "s/ZZZtemp/$temp/g" in.micelle_modif > in.micelle
echo "-- -- replaced temperature parameter with $temp"

echo "-- -- started lammps simulation for $temp"
srun -N 1 --ntasks-per-node=8 -J lammps_vernovskaya --comment="Lammps micelle run" -p RT ~/bin/lmp_mpi -in in.micelle
echo "-- -- finished"

mv dump.micelle dump.micelle_$temp

echo "-- -- running awk for $temp"
awk -v temp=$temp -f ../awk_energy.sh log.lammps

temp=`echo $temp $temp_step | awk '{print $1 + $2}'`
rm in.micelle
rm log.lammps

done

echo "-- -- started making pickle from dump.micelle for"
python3 ../pickle_input_data.py $num_params
echo "-- -- finished pickle"

echo "-- -- started calculating msd for"
python3 ../msd.py $num_params
echo "-- -- finished msd"

echo "-- -- making energies plot in gnuplot"
gnuplot -persist <<-EOFMarker
set terminal png size 800, 600
set output "energies.png"
set datafile separator ' '
set grid xtics ytics
set ylabel "Energy"
set xlabel 'Step'
set title "Energies with different starting temperatures" 
plot "energies_0.txt" using 1:2 with lines title "temp 0", "energies_0.15.txt" using 1:2 with lines title "temp 0.15", "energies_0.3.txt" using 1:2 with lines title "temp 0.3", "energies_0.45.txt" using 1:2 with lines title "temp 0.45",  "energies_0.6.txt" using 1:2 with lines title "temp 0.6"
EOFMarker
echo "-- -- finished plot"

echo "-- -- making matplotlib plot"
python3 ../matplotlib_plot_maker.py $num_params 50
echo "-- -- finished plot"

echo "-- -- sending telegram messages"
curl -s -X POST https://api.telegram.org/bot1692780481:AAEgf_iLfjGG3hThdu52fN8ob7GiGNncawc/sendPhoto -F chat_id=576139175 -F photo="@energies.png" -F caption="Script for micelle is finished. Plots for energies:"
curl -s -X POST https://api.telegram.org/bot1692780481:AAEgf_iLfjGG3hThdu52fN8ob7GiGNncawc/sendPhoto -F chat_id=576139175 -F photo="@msds_plt.png" -F caption="Plots for MSDs"
echo "-- -- sent messages"

echo "-- finished all"
