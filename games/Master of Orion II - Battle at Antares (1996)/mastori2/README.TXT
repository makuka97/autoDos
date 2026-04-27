===========================================================

         MASTER OF ORION II:
         Battle at Antares
            Version 1.31

            Readme File
           11 April 1997
===========================================================

How to Update to Version 1.31
=============================
1) Download the updater file named "MOO2V131.ZIP." Please be 
   sure to note which directory you download the file to.

2) Copy MOO2V131.ZIP to the Master of Orion II directory on
   your hard drive. This directory is usually \MPS\ORION2
   (for the DOS version) or \PROGRA~1\MICROP~1\ORION2
   (for the Windows 95 version). For example, you would
   type "COPY MOO2V131.ZIP C:\MPS\ORION2" at the DOS prompt
   if you installed the DOS version.

3) To update your copy of Master of Orion II to version
   1.31, extract the files in MOO2V131.ZIP by using a 
   utility such as Pkunzip or WinZip. New files will then 
   overwrite older versions of the same files.

4) You can read about the changes in version 1.31 either 
   in this Readme file or the text file named "README.TXT" 
   in the Master of Orion II directory.


Network
=======
The Windows 95 network mode requires both Microsoft Client 
and IPX protocol.

Unfortunately, the DOS and Windows 95 versions of the game 
are not compatible across the network. Therefore, you cannot
play head-to-head if you are playing the DOS version and 
another player is using the Windows 95 version. All players 
wishing to play in a network game must use the same version 
(DOS or Windows 95).

In addition, all players must be using the same version
number of the game (such as version 1.31).

Once you have selected "JOIN" in a network game, you will 
not be able to cancel.

TEN is only supported in the Windows 95 version of the game.

We suggest that the player with the fastest computer be the
one to start the multiplayer game.


Modem
=====
Unfortunately, the DOS and Windows 95 versions of the game
are not compatible over modem. Therefore, you cannot play
head-to-head if you are playing the DOS version and another
player is using the Windows 95 version. Both players
wishing to play a modem game must use the same version 
(DOS or Windows 95).

In addition, both players must be using the same version
number of the game (such as version 1.31).

If you are having problems playing a head-to-head game
over modems, we suggest trying the following:

1) Click on the "Multiplayer Setup" screen.
2) Click on the "Modem" and "Comm Info" buttons.
3) Change "Baud Rate" to "38400."
4) Erase "ATZ" from the "Clear String" field.

Note: If you are still unsuccessful at connecting,
please try lowering the "Baud Rate" to "14400." Make
sure that both you and your friend choose the same
baud rate.

We also recommend disabling all error correction and
data compression in your modem. You will need to refer 
to your owner's manual to find out how to do this.

The DOS version of the game will not work with 
nonstandard IRQs for your COM port. For example, COM
1 should be IRQ 4, COM 2 should be IRQ 3, COM 3
should be IRQ 4, and COM 4 should be IRQ 3. If your
COM port is set to something other than those (such
as COM 3 set to IRQ 5), then the DOS version will
not connect over a modem.

Watch out for IRQ conflicts with your mouse. If your
serial mouse and COM port share the same IRQ, you will 
not be able to use your modem for a head-to-head game.


8MB RAM Version
===============
If you have only 8MB RAM, do not load any extended memory 
manager (such as EMM386 or QEMM) or else the game will not have 
enough free memory to run. You can also try running EMM386 with 
no parameters ("device=c:\directory\emm386.exe").

Games created on a computer with 8MB RAM or network games 
involving a computer with only 8MB RAM will not have nebulae.

If you are playing the Windows 95 version, you must set 
Virtual Memory to be at least 16MB. To do this, select
"System" from your Control Panels. Click the "Performance"
tab and then the "Virtual Memory" button. Set "Minimum"
to "16."


Video
=====
If you have an older video card that is not supported by
Microsoft's DirectX, we recommend that you play the DOS
version of Master of Orion II. Otherwise, if you install 
the DirectX drivers while installing the Windows 95 version 
of the game, the DirectX drivers may overwrite your 
existing Windows 95 video drivers.
 

Changes and Additions to the Game
=================================
The following items were changed or added after the manual 
had already gone to print.

Custom Race Screen
------------------
-1 food was changed to -0.5 food and its cost changed 
to -3.

A new special has been added. "Poor home world" costs -1
and makes your home world mineral poor.

Ship defense bonuses have been increased from +20 to +25
and from +40 to +50 at the same cost.

Tactical Combat
---------------
When playing tactical combat vs. a computer-controlled
empire, there is a super-fast resolution mode. Press the 
"Z" key to turn on the super-fast mode. Click anywhere to 
turn off the super-fast mode. Combat graphics displays are 
minimal in super-fast mode, greatly speeding play.

Hall of Fame
------------
To reset the Hall of Fame high scores, press Alt-C. This will
restore the default scores.

Star Name
---------
After you colonize a planet for the first time, you will be
allowed to enter a new star name. The length of the new name
will be limited by the amount of horizontal space available
on the main galaxy map. Bear in mind that each letter takes
up a different amount of space. (For example, a "W" is wider 
and takes up more space than an "I."). In any case, you will
be limited to 15 characters.


Version 1.31 Changes
====================

New Features
------------
Tactical combat ship initiative is now an option on the Game/Settings 
screen. When this option is enabled, ships in combat will move in 
the order of their initiative rating. The initiative rating is equal 
to the ship's total beam offense bonus divided by 10 plus the ship's 
current combat speed [Offense/(10+speed)]. Thus, smaller ships should
move before bigger, slower ones.

Bug Fixes
---------
The occurrence of "You are too powerful" messages from the computer 
AIs has been reduced. Various other changes to decrease the erratic 
behavior of computer AIs in diplomacy (such as races declaring war on
you for economic expansion) have also been made.

If two races own planets in the same system, the colors of the labels
now reflect that in the Windows 95 version.

All ships in a fleet are removed from a system if that race accepts
your demand to so, instead of just the ships with weapons.

Using the Alt-CRUNCH cheat now triggers the cheat warning in
multiplayer games.

The Hall of Fame now records players' high scores.


Version 1.3 Changes
===================

New Features
------------
The last customized race created will be saved. It can be loaded by 
clicking on the "Last Race" button instead of selecting a picture 
for your custom race to use.

Customized races can now be named by their creator. Just click on 
the race name in the top middle of the Race Customization screen to 
edit the name.

Individual ships can be renamed using the detailed ship display. 
This display is reached by right-clicking on a ship in the Fleet 
Movement pop-up list, the Fleet Operations screen or the Leaders 
screen. In the detailed ship display, left-click on the ship's name 
to enter a new ship name.

When refitting a ship, you will be prompted to select a current 
ship design if there are any of the same size class as the ship to 
be refitted. The refitted ship will have its design updated to the 
chosen design's specifications. The design screen will still be 
available as an option as in earlier versions.

In tactical combat, pressing "T" will end the current player's turn.

Tutor level should be a little easier.

Left-click on the marines displayed at the bottom of the Colony 
screen to display your current ground combat statistics.

Rules Changes 
-------------
The attacker will now always move first in tactical battles, except
for the Antarans who will always move first regardless.

The Damper Field will block any marine casualties caused by Neutron 
Blasters and Death Rays.

Ion Pulse Cannons now take 30 space, do 2-10 points of damage and 
cannot be modified to be Heavy Mount.

Gyro-Destabilizers now take 75 space and cost 50BC. Their damage 
has also been decreased to 1-4 per size class of target ship.

Plasma Cannons have been increased to 25 space.

The Creative racial ability now costs 8 picks. As a result, the base 
Psilon race loses Artifact home world and gains Large home world.

Fighters have a 50% chance to avoid the effects of any ship 
self-destruct or warp core breach explosions.

The Custom Race option is available on all difficulty levels.

Extra combat turns given by the Time Warp Facilitator will be given 
after the opponent has taken a turn.

    1st player: normal turn
    2nd player: normal turn
    1st player: extra turn
    2nd player: extra turn

Assault shuttles are now one-shot weapons. They land their marines, 
but do not return to the launching ship.

Bug Fixes
---------
Modem problems with head-to-head play have been addressed.

An option for the fast refit of ships has been added. 

The lockup when all the ships on one side are in stasis is corrected.

Ships will now be able to reach Elite crew status.

Ships in stasis will not take damage from ship explosions.

Human players may now give Antaran technology to each other.

If your income is negative and you are giving tribute to another
player, you give them zero BCs instead of a negative amount of BCs.

Leaders give their special technology when hired, even if hired on 
a later turn.

The player will now benefit from Loknar's Galactic Lore skill.

It used to be possible to circumvent the 5-turn ETA by sending the
leader to the pool and then back to the same star system. This has 
been fixed.

Scrapping (captured) ships now gives you the opportunity to learn 
improved fuel cell technology.

You can now able to hire "special" leaders.

Asteroids were added to the Colony system display.

The Tiny planetary shield crash bug is fixed.

Graphical problems with planetary shields have been fixed.

The Colony Building Queue screen is changed to list the planet name.

If you press the "<" and ">" keys on the Colony screen and the 
Colony Building Queue screen, you will automaticaly skip the 
outposts in the lists.

Captured ships with officers can no longer be refitted on the refit
pop-up menu.

On the Fleets screen, the relocation hot-key has been changed to F5.
The hot-key for cancelling all relocations has been changed to Alt-F5.


Version 1.2 Changes
===================
The following items no longer crash the game:
 
  * The game no longer crashes in space combat if the Antarans
    capture ships.

  * The game no longer crashes if you cycle through the opening
    menus.

  * The game no longer crashes if the name of the home system has
    too many letters.

  * The game no longer crashes if the player wins by being voted 
    leader of the galaxy and the name of that player's emperor is
    longer than 10 characters.

The game can now play head-to-head over a null-modem serial
connection more reliably.

The Hall of Fame now records players' high scores.

The Hall of Fame now supports longer emperor names.

Evolutionary Mutation will now correctly give the player 4
points to distribute instead of a random amount.

Offering gifts to other races will no longer hurt the
player's diplomatic relationship.

When a system is demanded in the diplomacy screen, the
proper message is sent to the other player.

Music no longer gets cut off when exchanging technologies
during hot-seat play.

Clicking Alt-spacebar no longer displays a drop-down menu.

Planetary shield graphics have been improved.

The hand icon no longer turns black before combat.

The bombing explosions no longer turn black if bombing
is resumed.

Assassin leaders now correctly kill an enemy spy when you're told
they do.

The overflow bug if you research more than 32,767 research points
per turn has been fixed. The number now truncates to 32,767. The
same fix was made for the player's income.

When you acquired the application you were currently researching
by nonresearch means (diplomacy, spying, etc.) and you were 
Creative or it was a gray box field, the game used to erroneously 
give you the whole field. The game will now correctly assign you 
to research some other application in that field (unless there 
are none, in which case you do get the field).

In an obscure rule change, there are now always some pre-allocated
ships for the humans in a single-player game. Before, the ship
slots were allocated round-robin among all players. In games with
very large number of ships, this meant that you might sometimes
only be able to build a few ships in a turn.

Players no longer get System Specials if there is a monster there
after combat. (This used to happen with eels since they don't 
attack you. It could also happen if two players showed up on the
same turn: the monster attacks one and then the second player 
chooses not to attack the monster.)

In a rule change, if both sides die in a battle vs. the Guardian,
the player will get the Loknar special now. (Previously, you had 
to actually win the battle, not just tie.)

A network synchronization bug involving viewing battle results 
when one player's computer was slower than the other has been 
fixed.


Customer Support
================
If you having problems with Master of Orion II, we can best
help you if (1) you are at your computer when you call and
(2) you have the following information handy:

* Version number of Master of Orion II
* Your computer's brand and model
* Your computer's BIOS brand and version number
* Total RAM installed in your computer
* Name and version number of your operating system (such
  as MS-DOS, Windows 3.1 or Windows 95)
* Name and version number of your memory manager (such as 
  QEMM, 386Max or EMM386)
* Version number of your DirectX drivers
* CD-ROM brand and model name
* Sound card brand and model name
* Mouse brand and version number of mouse driver
* The size of your Windows swap file
* The exact error message displayed (if any)
* Contents of AUTOEXEC.BAT and CONFIG.SYS files
* At the DOS prompt, type "mem/c" and write down the 
  information onscreen

MSD Report
----------
Occasionally, Customer Support may request an MSD report 
from you. MSD is a diagnostic program that can help 
establish the cause of most compatibility problems on your 
computer while attempting to run our games. This program 
is supplied with all versions of DOS and Windows. However,
Windows 95 users will first need to copy the program from
the Windows 95 CD-ROM to the hard drive by typing the 
following command at the DOS prompt:

  copy d:\other\msd\msd.exe c:\windows\command

To generate your MSD report, first exit Windows 3.1 or 
Windows 95. Place a formatted floppy disk in drive A and 
type the following at the DOS prompt:

  msd /f a:report.txt

You can then print this report or send the file on the 
floppy disk to MicroProse (should this be required).

How to Contact Customer Support
-------------------------------
Have a pen and paper handy when you call. You can also write
to Customer Support at the address shown below.

Due to the many different hardware and software configurations
available for modern computers, you may still have to talk to 
your computer dealer or hardware supplier in order to get our
game to run with their product.

USA:
----
MicroProse Customer Support
2490 Mariner Square Loop
Alameda, CA 94501
Telephone: (510)522-1164 (9:OO am-5:00 pm Pacific Time) 
Fax: (510)522-9357

United Kingdom:
---------------
MicroProse
The Ridge
Chipping Sodbury, South Glos BS17 6BN
Telephone: +44 (0) 1454 893900 (0900-1730 GMT/BST)
Fax: +44 (0) 1454 894296

Germany:
--------
MicroProse
Bartholomausweg 31
33334 Gutersloh
Telephone: +49 (0) 5241 946480 (Monday to Wednesday 1400-1900)
Fax: +49 (0) 5241 946494

France:
-------
Electronic Arts
Centre d'Affaires Telebase
3 rue Claude Chappe
69771 St. Didier au Mont d'Or Cedex
Telephone: +33 (04) 72 53 25 00

Bulletin Boards:
----------------
United Kingdom	+44 (0)1454 327083 (14,400 baud)
Germany	  	+49 (0)5241 946484 (28,800 baud)
USA             (510)522-8909      (14,400 baud)

America Online:
---------------
Send e-mail to MicroProse Customer Support at "MPS1." Press 
Ctrl-K for "Go to Keyword" and enter "MicroProse" to reach 
MicroProse's forum and library areas.

CompuServe:
-----------
MicroProse-Europe       71333,314
MicroProse-Germany	74777,3326
MicroProse-USA  	76004,2223

Type "GO GAMBPUB" and select "Section 2" to reach MicroProse's 
forum and library areas. 

Internet:
---------
Send e-mail to MicroProse Customer Support at support@microprose.com
(or if you're in Germany to service@microprose.de).

FTP:
----
The MicroProse FTP site features a complete library of the latest 
updates, demos and product information. The address is:
  ftp.microprose.com

World Wide Web:
---------------
To access our Web site, use your Web browser software to point to:
  http://www.microprose.com


Software Fault
==============
In the unlikely event of a software fault, please return the
complete package, with your receipt, to the place of purchase.


=============
This documentation, accompanying manual and CD are copyrighted.
The owner of this product is entitled to use this product for
his or her personal use. Except for the quoting of brief
passages for the purposes of reviews, no one may transfer, copy,
back-up, give or sell any part of the manual or the information
on the CD, or transmit in any form or by any means, electronic,
mechanical, photocopying, recording or otherwise without the
prior permission of the publisher. Any person or persons
reproducing any part of this program, in any media, for any
reason, shall be guilty of copyright violation and shall be
subject to civil liability at the discretion of the copyright
holder. Not for rent or hire.

Made in the USA/UK
