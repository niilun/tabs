#!/bin/bash
cd ..

echo Running pyinstaller...
pyinstaller --onefile --icon=assets/logos/logo.xbm --hidden-import=PIL._tkinter_finder --add-data "units:units" main.py

echo Moving executable to root folder...
cd dist
mv main ..
cd ..
mv main TABS-linux

echo Removing leftover folders...
rm -dr build
rm -dr dist
rm main.spec

echo Build complete! To run go back to the root tabs folder and use \'./TABS-linux.\'
echo IMPORTANT! if you\'re zipping this executable keep the 
echo units/ \& assets/ folders at the same level as the executable.