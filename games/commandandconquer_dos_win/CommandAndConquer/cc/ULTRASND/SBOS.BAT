@ECHO OFF
REM ----
REM  Name:    SBOS Batch File
REM  Tested:  01/06/94 - JRS
REM  Purpose: Check for the users ULTRADIR enviro variable. If found then
REM           use this to find SBOS. This is more reliable then using
REM           the path to locate these files.
REM  Revised: 02/07/94 - Force SBOSDRV.COM so it will not conflict with EXE
REM           02/11/94 - Only force SBOSDRV.COM if it exist. Otherwise load
REM                      SBOSDRV.EXE
REM           02/23/94 - Put LH command when loading SBOSDRV.EXE
REM           04/06/94 - JL - Modified so SBOS in current dir has presidence(SP?)
REM ---
REM See if SBOS in current dir
REM ---
if not exist loadsbos.exe GOTO NOT_CURR
if exist sbosdrv.com sbosdrv.com
if exist sbosdrv.com GOTO LCURRDIR
if not exist sbosdrv.exe GOTO NOT_CURR
LH sbosdrv.exe
:LCURRDIR
loadsbos %1 %2 %3 %4
GOTO EXIT

:NOT_CURR
REM ---
if %ultradir%!==! GOTO NOULTRADIR
REM ---
REM   Check to see if we are to load SBOSDRV.COM or SBOSDRV.EXE
REM ---
if exist %ultradir%\sbosdrv.com %ultradir%\sbosdrv.com
if exist %ultradir%\sbosdrv.com GOTO LOADSBOS
if exist %ultradir%\sbosdrv.exe LH %ultradir%\sbosdrv.exe
if exist %ultradir%\sbosdrv.exe GOTO LOADSBOS
ECHO Unable to locate SBOS file(s) - (SBOSDRV). Make sure you are running
ECHO SBOS from the same directory you installed the UltraSound software.
GOTO EXIT

:NOULTRADIR
if exist sbosdrv.com sbosdrv.com
if exist sbosdrv.com GOTO NLOADSBOS
if exist sbosdrv.exe LH sbosdrv.exe
if exist sbosdrv.exe GOTO NLOADSBOS
ECHO Unable to locate SBOS file(s) - (SBOSDRV). Make sure you are running
ECHO SBOS from the same directory you installed the UltraSound software.
GOTO EXIT

:LOADSBOS
if exist %ultradir%\loadsbos.* %ultradir%\loadsbos %1 %2 %3 %4
if exist %ultradir%\loadsbos.* GOTO EXIT
ECHO Unable to locate SBOS file(s) - (LOADSBOS). Make sure you are running
ECHO SBOS from the same directory you installed the UltraSound software.
GOTO EXIT

:NLOADSBOS
if exist loadsbos.* loadsbos %1 %2 %3 %4
if exist loadsbos.* GOTO EXIT
ECHO Unable to locate SBOS file(s) - (LOADSBOS). Make sure you are running
ECHO SBOS from the same directory you installed the UltraSound software.
GOTO EXIT

:EXIT
