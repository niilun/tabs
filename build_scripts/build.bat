@echo off
cd ..

echo Running pyinstaller...
pyinstaller --onefile --icon=resources/logos/logo.ico main.py

echo Moving executable to root folder...
move dist\main.exe .
ren "main.exe" "TABS.exe"

echo Removing leftover folders...
rmdir /s /q build
rmdir /s /q dist
del main.spec

echo Build complete! To run double click 'TABS.exe'.