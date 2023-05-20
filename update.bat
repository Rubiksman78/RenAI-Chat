@echo off
git fetch origin
git reset --hard main
"libs/pythonlib/python.exe" -m pip install --force-reinstall -r requirements.txt
