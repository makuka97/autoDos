@ECHO OFF
@BREAK ON
CLS
IF %ULTRADIR%!==! GOTO NOCARD
GOTO START
:NOCARD
ECHO Unable to locate your UltraSound environment variable (ULTRADIR).
ECHO ÿ
ECHO Note:
ECHO If you have just installed the UltraSound, this is because you have
ECHO not rebooted your system.
ECHO ÿ
GOTO DONE
:START
ECHO ÿ
ECHO Welcome to UltraSound MIDI Demoÿ
ECHO ÿ
ECHO The following MIDI files will be played.
ECHO You can skip to the next file by pressing any key;
ECHO or you can quit at any time by pressing CTRL+C.
ECHO ÿ
ECHO - Good Vibesÿ
ECHO - Hero                by K. Goach
ECHO - Hide 'n' Seek
ECHO - Jesu Joy of Man's Desiring
ECHO - Latin Dance
ECHO - Minuet in G
ECHO - Piano Heaven
ECHO - She's so funky      by S. Yoshida, E. Bell, K. Goach & P. Tucker
ECHO - Strivingÿ
ECHO -ÿSwing Cafe
ECHO -ÿTechno 78
ECHO -ÿThe Rain            by K.Goach
ECHO - Tocatta and Fugue in D Minorÿ
ECHO - Yellow Rose of Texas
ECHO ÿ
ECHO ÿ
PAUSE
REM ***
@ECHO Loading "Good Vibes"                      1 of 14
@ECHO Press any key to advance to next song, or CTRL+C to exit.
playmidi -v120 %ULTRADIR%\MIDI\gdvib6 -x24
@if errorlevel 99 goto done
REM ***
@ECHO Loading "Hero" (K. Goach)                 2 of 14
@ECHO Press any key to advance to next song, or CTRL+C to exit.
playmidi -v120 %ULTRADIR%\MIDI\HERO -x26
@if errorlevel 99 goto done
REM ***
@ECHO Loading "Hide 'n' Seek"                   3 of 14
@ECHO Press any key to advance to next song, or CTRL+C to exit.
playmidi -v110 %ULTRADIR%\MIDI\hidnseek -x28
@if errorlevel 99 goto done
REM ***
@ECHO Loading "Jesu Joy of Man's Desiring"      4 of 14
@ECHO Press any key to advance to next song, or CTRL+C to exit.
playmidi -v110 %ULTRADIR%\MIDI\jesujoy -x20
@if errorlevel 99 goto done
REM ***
@ECHO Loading "Latin Dance"                     5 of 14
@ECHO Press any key to advance to next song, or CTRL+C to exit.
playmidi -v120 %ULTRADIR%\MIDI\latindnc
@if errorlevel 99 goto done
REM ***
@ECHO Loading "Minuet in G"                     6 of 14
@ECHO Press any key to advance to next song, or CTRL+C to exit.
playmidi -v110 %ULTRADIR%\MIDI\minuetg -x20
@if errorlevel 99 goto done
REM ***
@ECHO Loading "Piano Heaven"                    7 of 14
@ECHO Press any key to advance to next song, or CTRL+C to exit.
playmidi -v120 %ULTRADIR%\MIDI\pnoheavn -x24
@if errorlevel 99 goto done
REM ***
@ECHO Loading "She's so funky" (S. Yoshida, E. Bell, K. Goach, P. Tucker) 8 of 14
@ECHO Press any key to advance to next song, or CTRL+C to exit.
playmidi -v120 %ULTRADIR%\MIDI\SOFUNKY.MID -x24
@if errorlevel 99 goto done
REM ***
@ECHO Loading "Striving"                        9 of 14
@ECHO Press any key to advance to next song, or CTRL+C to exit.
playmidi -v120 %ULTRADIR%\MIDI\striving -x28
@if errorlevel 99 goto done
REM ***
@ECHO Loading "Swing Cafe"                      10 of 14
@ECHO Press any key to advance to next song, or CTRL+C to exit.
playmidi -v120 %ULTRADIR%\MIDI\SWNGCAFE
@if errorlevel 99 goto done
REM ***
@ECHO Loading "Techno 78"                        11 of 14
@ECHO Press any key to advance to next song, or CTRL+C to exit.
playmidi -v120 %ULTRADIR%\MIDI\techno78 -x26
@if errorlevel 99 goto done
REM ***
@ECHO Loading "The Rain" (K. Goach)              12 of 14
@ECHO Press any key to advance to next song, or CTRL+C to exit.
playmidi -v120 %ULTRADIR%\MIDI\THE_RAIN.MID -x24
@if errorlevel 99 goto done
REM ***
@ECHO Loading "Tocatta and Fugue in D Minor"     13 of 14
@ECHO Press any key to advance to next song, or CTRL+C to exit.
playmidi -v110 %ULTRADIR%\MIDI\Tocatta
@if errorlevel 99 goto done
REM ***
@ECHO Loading "Yellow Rose of Texas"             14 of 14
@ECHO Press any key to advance to next song, or CTRL+C to exit.
playmidi -v120 %ULTRADIR%\MIDI\yelowros
@if errorlevel 99 goto done
REM ***
:done
@ECHO Thank you for choosing UltraSound!

