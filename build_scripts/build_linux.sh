#!/bin/bash
cd ..

echo Running pyinstaller...
pyinstaller --onefile --icon=resources/logos/logo.xbm main.py

echo Moving executable to root folder...
cd dist
mv main ..
cd ..
mv main TABS-linux

echo Removing leftover folders...
rm -dr build
rm -dr dist
rm main.spec

echo Build complete! To run go back to the root tabs folder and use './TABS-linux.'