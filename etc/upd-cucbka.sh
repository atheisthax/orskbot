today=$(date +"%Y-%m-%d")
printf $today
newname="cucbka-"${today}
printf $newname
cp cucbka.dat ${newname}.dat
python3 cucbka.py
mv cucbka1.dat cucbka.dat
