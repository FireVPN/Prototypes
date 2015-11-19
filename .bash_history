echo "Dies ist das Hauptverzeichnis von FireVPN"
echo "Dies ist das Hauptverzeichnis von FireVPN" > README.txt
git init
git add README.txt
git commit -m "Readme hinzugefügt"
git config --global user.email "elias.eckenfellner@edu.htl.rennweg.at"
git config --global user.name "eliaseckenfellner"
git commit -m "Readme hinzugefügt"
git remote add origin https://github.com/FireVPN/FireVPN.git
git push -u origin master
exit
