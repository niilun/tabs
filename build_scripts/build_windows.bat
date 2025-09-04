@echo off
cd ..

echo Running pyinstaller...
pyinstaller --onefile --icon=assets/logos/logo.xbm --hidden-import=PIL._tkinter_finder --add-data "units:units" main.py

echo Moving executable to root folder...
move dist\main.exe .
ren "main.exe" "TABS-win.exe"

echo Removing leftover folders...
rmdir /s /q build
rmdir /s /q dist
del main.spec

echo Build complete! To run double click 'TABS-win.exe'.
echo IMPORTANT! if you're zipping this executable keep the units/ & assets/ folders
echo at the same level as the executable.