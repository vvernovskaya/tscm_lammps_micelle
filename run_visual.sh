#!/bin/bash

num_params=5
n_steps=6000

echo "-- started making visualization"

curl -s -X POST https://api.telegram.org/bot1692780481:AAEgf_iLfjGG3hThdu52fN8ob7GiGNncawc/sendMessage -d chat_id=576139175 -d text="Started making video for micelle."

ovitos -nt 4 ../micelle_ovito_vis.py $n_steps

curl -s -X POST https://api.telegram.org/bot1692780481:AAEgf_iLfjGG3hThdu52fN8ob7GiGNncawc/sendMessage -d chat_id=576139175 -d text="Finished making video for micelle."

echo "-- -- finished video"

rm log.txt

echo "-- -- sending video to telegram"
curl -s -X POST https://api.telegram.org/bot1692780481:AAEgf_iLfjGG3hThdu52fN8ob7GiGNncawc/sendVideo -F chat_id=576139175 -F video="@micelle.mp4" -F caption="Visualization of micelle"
echo "-- -- video is sent"

echo "-- finished visualization script"
