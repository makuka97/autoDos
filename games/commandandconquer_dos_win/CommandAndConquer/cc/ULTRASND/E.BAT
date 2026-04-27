@ECHO OFF
@BREAK OFF
REM ----------
REM Title:    UltraSound Emulation Picker
REM Purpose:  Give the user one common way to load any of the 3 Gravis
REM           emulators. Features include:
REM           1) Check for presense of ULTRASND & ULTRADIR
REM           2) Unload other emulators if necessary
REM           3) Allow user to pass command line arguments to emulators
REM           4) Allow user to specify without a menu what emulation to load
REM           5) Let the user know what emulation is currently active
REM           6) Make sure the necessary files are there to load
REM USAGE:
REM   GUSEMU What you want to Check
REM      1  - Wait for key press and return number
REM          10 - What emulation is currently loaded?
REM               0 = None 1 = SBOS 2 = UltraMid 3 = Mega-Em
REM
REM      11 - Is SBOS loaded?     1 = True  0 = False
REM      12 - Is UltraMID loaded?
REM      13 - Is Mega-Em loaded?
REM
REM      20 - Remove SBOS      1 = Successfull  0 = Failed
REM      21 - Remove UltraMID
REM
REM Modified:
REM ----------
REM ==========
REM   Quick check to see if GUS has been installed and configured
REM ==========
IF %ULTRASND%!==! GOTO NOGUS
IF %ULTRADIR%!==! GOTO NOGUS
IF %1!==!         GOTO START
IF %1==1          GOTO SBOS
IF %1==2          GOTO ULTRAMID
IF %1==3          GOTO MEGAEM
IF %1==4          GOTO REMOVE
:START
CLS
ECHO  ษอออออออออออออออออออออออออออออออออออออออออออออออออออออป
ECHO  บ        Gravis UltraSound Emulation Manager          บ
ECHO  บ                    Version 1.0                      บ
ECHO  บ                                                     บ
GUSEMU 11
IF ERRORLEVEL 1 ECHO  บ Currently In: Sound Blaster emulation               บ
GUSEMU 12
IF ERRORLEVEL 1 ECHO  บ Currently In: UltraMID (AIL)                        บ
GUSEMU 13
IF ERRORLEVEL 1 ECHO  บ Currently In: GM/SCC1/MT32 and Sound Blaster mode   บ
ECHO  บ  1 = Sound Blaster emulation                        บ
ECHO  บ  2 = UltraMID (AIL)                                 บ
ECHO  บ  3 = Mega-Em - GM/SCC1/MT32 and Sound Blaster       บ
ECHO  บ  4 = Remove all emulations                          บ
ECHO  บ  5 = Exit                                           บ
ECHO  บ                                                     บ
ECHO  บ  Which emulation do you wish to activate?           บ
ECHO  ศอออออออออออออออออออออออออออออออออออออออออออออออออออออผ
GUSEMU 1
IF ERRORLEVEL 5 GOTO STOP
IF ERRORLEVEL 4 GOTO REMOVE
IF ERRORLEVEL 3 GOTO MEGAEM
IF ERRORLEVEL 2 GOTO ULTRAMID
IF ERRORLEVEL 1 GOTO SBOS
GOTO EXIT

:MEGAEM
IF NOT EXIST %ULTRADIR%\MEGAEM.EXE        GOTO MISSING
IF NOT EXIST %ULTRADIR%\EMUSET.EXE        GOTO MISSING
CLS
IF %2!==! GOTO MEGALOAD
GOTO EMUSET
:MEGALOAD
MEGAEM %2 %3 %4 %5
:EMUSET
EMUSET %2 %3 %4 %5
GOTO EXIT

:ULTRAMID
IF NOT EXIST %ULTRADIR%\ULTRAMID.EXE      GOTO MISSING
IF NOT EXIST %ULTRADIR%\MIDI\ULTRAMID.INI GOTO MISSING
GUSEMU 11
IF ERRORLEVEL 1 GUSEMU 20
GUSEMU 12
IF ERRORLEVEL 1 GOTO LOADED
GUSEMU 13
IF ERRORLEVEL 1 %ULTRADIR%\MEGAEM /U
CLS
%ULTRADIR%\ULTRAMID %1 %2 %3 %4
GOTO EXIT

:SBOS
IF NOT EXIST %ULTRADIR%\SBOS.BAT           GOTO MISSING
IF NOT EXIST %ULTRADIR%\SBOSDRV.*          GOTO MISSING
IF NOT EXIST %ULTRADIR%\LOADSBOS.EXE       GOTO MISSING
IF NOT EXIST %ULTRADIR%\SBOS\SBOSLIB.SBS   GOTO MISSING
IF NOT EXIST %ULTRADIR%\SBOS\SBOS.CFG      GOTO MISSING
GUSEMU 11
IF ERRORLEVEL 1 GOTO LOADED
GUSEMU 12
IF ERRORLEVEL 1 GUSEMU 21
GUSEMU 13
IF ERRORLEVEL 1 %ULTRADIR%\MEGAEM /U
CLS
CALL %ULTRADIR%\SBOS.BAT %1 %2 %3 %4
GOTO EXIT

:REMOVE
GUSEMU 11
IF ERRORLEVEL 1 GUSEMU 20
GUSEMU 12
IF ERRORLEVEL 1 GUSEMU 21
GUSEMU 13
IF ERRORLEVEL 1 %ULTRADIR%\MEGAEM /U
ECHO  ษอออออออออออออออออออออออออออออออออออออออออออออออออออออป
ECHO  บ  Emulations removed.                                บ
ECHO  ศอออออออออออออออออออออออออออออออออออออออออออออออออออออผ
ECHO ÿ
GOTO EXIT

:NOGUS
ECHO 
ECHO  ษอออออออออออออออออออออออออออออออออออออออออออออออออออออป
ECHO  บ  Unable to locate your UltraSound card. Please      บ
ECHO  บ  run SETUP from your UltraSound directory.          บ
ECHO  ศอออออออออออออออออออออออออออออออออออออออออออออออออออออผ
ECHO ÿ
GOTO EXIT

:LOADED
ECHO 
ECHO  ษอออออออออออออออออออออออออออออออออออออออออออออออออออออป
ECHO  บ  Emulation is currently active.                     บ
ECHO  ศอออออออออออออออออออออออออออออออออออออออออออออออออออออผ
ECHO ÿ
GOTO EXIT

:MISSING
ECHO 
ECHO  ษอออออออออออออออออออออออออออออออออออออออออออออออออออออป
ECHO  บ  One or more of the files required to run the       บ
ECHO  บ  Emulation selected is can not be found! Please     บ
ECHO  บ  check your AUTOEXEC.BAT file to make sure the      บ
ECHO  บ  SET ULTRADIR= line is pointing to the correct      บ
ECHO  บ  directory.  If it is pointing to your UltraSound   บ
ECHO  บ  directory and you still get this error then the    บ
ECHO  บ  required files may be missing.  If so please       บ
ECHO  บ  re-install your UltraSound software to correct     บ
ECHO  บ  this problem.                                      บ
ECHO  ศอออออออออออออออออออออออออออออออออออออออออออออออออออออผ
ECHO ÿ
GOTO EXIT

:STOP
ECHO ÿ
GOTO EXIT

:EXIT


