@echo off
IF %ULTRADIR%!==! goto noultradir
IF %1!==! goto load
IF %1==-f goto unload
IF %1==/f goto unload
@ECHO Usage: Type MAXSBOS    to load MAXSBOS
@ECHO        Type MAXSBOS /f to unload MAXSBOS
GOTO end
:load
%ULTRADIR%\MAXSBOS\driver
%ULTRADIR%\MAXSBOS\loader
goto end
:unload
%ULTRADIR%\MAXSBOS\loader /f
GOTO end
:noultradir
@echo.
@echo Error: The ULTRADIR environment variable is missing.
@echo        Remeber to reboot the machine after running SETUP.
@echo.
:end
@echo on
