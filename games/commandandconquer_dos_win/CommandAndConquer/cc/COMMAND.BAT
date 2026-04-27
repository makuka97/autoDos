@echo off
rem Batchfile by HOSON/HYBRID 950926
if not exist CONQUER.INI goto nosetup:
hybrid
select.com
c&c.exe
cls
@echo Thanks for choosing Hybrid! We know we rule... :)-
goto end:

:nosetup
cls
echo Please run 'SETUP' first.
goto end:

:end