BEGIN{
read_flag=0
}

{
if ($1 == "Loop") {
read_flag=0
}
if (read_flag==1) {
printf "%f",$5 >> "energies.txt"
printf "\n" >> "energies.txt"
}
if ($1 == "Step") {
read_flag=1
}
}

END{

}
