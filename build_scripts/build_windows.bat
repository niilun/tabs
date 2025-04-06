@echo off
cd ..

echo Running pyinstaller...
pyinstaller --onefile --icon=assets/logos/logo.ico main.py

echo Moving executable to root folder...
move dist\main.exe .
ren "main.exe" "TABS-win.exe"

echo Removing leftover folders...
rmdir /s /q build
rmdir /s /q dist
del main.spec

echo Build complete! To run double click 'TABS-win.exe'.