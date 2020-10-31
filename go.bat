start /b /min .\bin\win_joytokey\JoytoKey.exe &
.\bin\win_ansicon\ansicon.exe -i
python.exe .\choreogrpah\choreograph.py
taskkill /f /im JoytoKey.exe
pause


