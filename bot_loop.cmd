rem @echo off
:loop

\.env\Scripts\activate.bat
python.exe bot.py 
goto loop