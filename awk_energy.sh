BEGIN{
read_flag=0
}

{
if ($1 == "Loop") {
read_flag=0
}
if (read_flag==1) {
printf "%d ",$1 >> "energies_"temp".txt"
printf "%f",$5 >> "energies_"temp".txt"
printf "\n" >> "energies_"temp".txt"
}
if ($1 == "Step") {
read_flag=1
printf "%s ","Step" >> "energies_"temp".txt"
printf "%s","Energy" >> "energies_"temp".txt"
printf "\n" >> "energies_"temp".txt"
}
}

END{

}
