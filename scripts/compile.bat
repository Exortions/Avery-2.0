@echo off
echo Deleting old folders...
del /f /s /q dist 1>nul
rmdir /s /q dist 1>nul
echo Compiling Avery 2.0 to dist/avery.exe...
pyinstaller --noconfirm --onedir --console --icon "img/Avery.ico" --name "avery"  "avery.py"
PAUSE
echo Cleaning up...
del /f /s /q __pycache__ 1>nul
del /f /s /q build 1>nul
rmdir /s /q __pycache__ 1>nul
rmdir /s /q build 1>nul
echo Successfully compiled Avery!