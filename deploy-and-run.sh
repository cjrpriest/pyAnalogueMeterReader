# get latest code and force working copy to reflect latest version
git fetch --all
git reset --hard master
cp ../pyAnalogueMeterReader.Config.py ./
python Main.py
