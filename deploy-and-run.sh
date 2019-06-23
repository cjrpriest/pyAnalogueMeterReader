# get latest code and force working copy to reflect latest version
git reset --hard master
git pull
cp ../pyAnalogueMeterReader.Config.py ./
python Main.py
