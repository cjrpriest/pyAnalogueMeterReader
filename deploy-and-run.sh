# get latest code and force working copy to reflect latest version
git pull
git reset --hard master
cp ../pyAnalogueMeterReader.Config.py ./
python Main.py
