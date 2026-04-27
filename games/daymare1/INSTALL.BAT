@echo off
echo This program creates a directory called "DAYMARE1" on drive C.
echo The program then copy the files into that directory.
pause
md c:\daymare1
copy *.dat c:\daymare1
copy *.doc c:\daymare1
copy daymare1.exe c:\daymare1
c:
cd c:\daymare1
echo Documentation is in a file called "README.DOC".
echo To start the game type in "DAYMARE1" and press the enter key.
@echo on
