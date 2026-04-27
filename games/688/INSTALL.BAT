echo off
cls
echo * Installing %1 %2 %3
if %1x == x goto NoParms
if %1 == a: goto OkSource
if %1 == b: goto OkSource
if %1 == A: goto OkSource
if %1 == B: goto OkSource
if %1 == c: goto NoSource
if %1 == d: goto NoSource
if %1 == C: goto NoSource
if %1 == D: goto NoSource
echo * Only A: and B: are allowed as source drives...
echo * Only C: and D: are allowed as destination drives...
goto NoParms
echo * 
goto NoParms

:OkSource
if %3 == c: goto OkDest
if %3 == d: goto OkDest
if %3 == C: goto OkDest
if %3 == D: goto OkDest
echo * Only C: and D: are allowed as destination drives...
echo *
goto NoParms

:OkDest
%1
cd\
if not exist 688.EXE goto WrongSrc
if not exist %1\MAXELL\*.* md %3\MAXELL
copy %1\*.* %3\MAXELL
copy %3\MAXELL\BAT.BAK %3\688.BAT
if not exist %3\MAXELL\688.EXE goto NoInstal
if not exist %3\MAXELL\688.MLB goto NoInstal
%3
goto GoodInst

:WrongSrc
echo * You specified %1 as your source drive, please place your MAXELL Preview disk
echo * into drive %1
echo *
pause
goto OkDest

:NoSource
A:
cd\
if not exist 688.EXE goto WrongSrc
if not exist %1\MAXELL\. md %1\MAXELL
copy A:\*.* %1\MAXELL
copy %1\MAXELL\BAT.BAK %1\688.BAT
if not exist %1\MAXELL\688.EXE goto NoInstal
if not exist %1\MAXELL\688.MLB goto NoInstal
%1
goto GoodInst

:GoodInst
cls
echo INSTALL has fininshed succesfully.
cd \MAXELL
dir 688.exe
goto Done

:NoInstal
echo * INSTALL reports that there was an error during installation.  Please check
echo * to see if you have enough free space on your hard disk (you need at least
echo * 360 K bytes free) and that you are using INSTALL correctly.
goto NoParms

goto done
:NoParms
echo * INSTALL will create a subdirectory named MAXELL at the root of your hard
echo * drive, then it will copy all the files from your copy of 688 ATTACK SUB
echo * to the MAXELL directory on your hard disk.
echo * Only hard drives C: or D: are allowed.
echo *   
echo * You must supply the letter for your hard drive.
echo * For example, if you want to copy to drive C:,
echo * type:
echo *              INSTALL C:
echo *   
echo * You can also specify floppy drive A: or B: as the drive containing your
echo * Maxell Preview disk.  Install will assume you are using drive A: unless you
echo * specify drive B:.  Only drive A: or B: are allowed. For example,
echo * if you want to install to hard drive D: from floppy drive B: type:
echo *  
echo *              INSTALL B: TO D:
echo *  
echo * Don't forget to type the 'TO' if you are using this second method...
goto Done

:Done
