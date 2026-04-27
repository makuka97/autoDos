                          COMMAND & CONQUER
                           [Version 1.07]

                 Copyright (C) 1995 Westwood Studios
 
 Topics covered in this README file:
 
 1. Autodetection of Sound Cards
 2. Known Sound Card Problems
 3. Windows Notes
 4. Keyboard Shortcuts and Special Features
 5. Modem Play Hints
 6. Network Play Hints
 7. Multi-CD machines and CD-changers
 8. Game updates and patches
 
 1. Autodetection of Sound Cards
 ===============================
 
 C&C utilizes sophisticated techniques to autodetect your sound card.
 Because of the vast number of machine configurations possible on PC's,
 C&C may not autodetect your sound card or it might misidentify the card.
 For this reason you should treat the detected card as a suggestion only.
 If you know that the detected card is definitely wrong you can override
 the selection and pick the correct card from the SETUP program.
 
 If you select a sound card that is not present in your machine, your machine
 may lock-up, or the sound card may stop responding. Either of these
 situations may be corrected by simply turning off the computer, waiting 15
 seconds and then turning it back on.
 
 2. Known Sound Card Problems
 ============================
 
         Windows 95
         ----------
         See the Windows section below for sound card notes.
 
         Creative Labs - Soundblaster 1.0/1.5 card
         -----------------------------------------
         These early Soundblaster cards do not support some of
         the features which are built into later versions of the
         card. This may result in lower audio quality on
         these cards.
 
         Soundblaster Compatible Cards
         -----------------------------
         The Soundblaster code in C&C is written for 100% Soundblaster
         compatible sound cards made by Creative Labs. If you have a
         Soundblaster compatible sound card from another manufacturer
         you may experience stuttering or popping in the sound, or even
         no sound at all.
 
         If you are unsure of the correct Port, IRQ and DMA settings
         for your Soundblaster compatible card, try typing SET from
         the DOS prompt. If your machine has been configured with a
         BLASTER environment variable in your AUTOEXEC.BAT file you
         should see a line similar to:
 
         SET BLASTER=A220 I5 D1 H5 T4
 
         The number after the A (i.e., 220 in this case) is your port address;
         the number after the I (5 in this case) is your IRQ and the number
         after the D (1 in this case) is your DMA channel setting. Armed with
         these numbers you can go ahead and manually select your soundcard
         from the SETUP program and enter the Port, IRQ and DMA in the boxes
         when prompted. If you have a Soundblaster 16 or AWE32 soundcard and
         you are having difficulty with autodetection, these same comments
         apply except that you may have to enter the number after the H as
         your DMA setting, depending on your configuration.
 
         Compaq Computers
         ----------------
         Some Compaq machines may not autodetect the installed sound
         card.  If this occurs, try selecting Sound Blaster Pro/Pro2
         from the SETUP program.
 
         Sound Galaxy Basic 16
         ---------------------
         This Soundblaster compatible card can sometimes be incorrectly
         autodetected as a Soundblaster Pro or Soundblaster 16, causing
         unpredictable results. We recommend that you manually select
         Soundblaster and enter the Port, IRQ and DMA values that
         correspond to your card. See the comments under Soundblaster
         compatible cards above.
         
         ESS AudioDrive
         --------------
         Under certain circumstances the autodetect code can incorrectly
         identify this card as a Soundblaster 16. If this occurs you will
         need to override this driver by selecting ESS AudioDrive with
         the correct values for your system.
 
         Adlib Gold
         ----------
         Under certain circumstances the autodetect code can return
         incorrect Port, IRQ and DMA settings. If you are having difficulty
         obtaining sounds on this sound card try manually selecting the
         card in the SETUP program and entering the correct Port, IRQ and
         DMA settings.
 
         Golden Sound Pro 16
         -------------------
         We have found that better results may be obtained on this
         sound card by reducing the game volume from the in-game
         sound control menu. Volume levels should be set to about
         half way.
 
         GRAVIS ULTRA SOUND
         ------------------
         Some Gravis Ultrasound owners may experience audio clipping
         and/or reduced game performance.  We recommend that you turn
         the volume for musical scores all the way down (off) to see
         if this helps.

         -----------------------------------------------------------
         If you continue to have trouble with your soundcard please
         consult the troubleshooting section of your soundcard manual
         or contact Westwood technical support as described in your
         C&C manual.

 3. Windows Notes
 ================
 
         Windows and Windows for Workgroups v.3.1 & v.3.11
         -------------------------------------------------
         C&C uses special code to launch itself from the Windows icon
         and will attempt to close any active Windows applications prior
         to running. You will not be able to access other Windows programs
         when C&C is active.
 
         This greatly enhances the performance and playability of the game
         on 486 class machines.
 
         Windows 95
         ----------
 
         Running through Windows 95:
 
         C&C's default behavior under Windows 95 is to run as a DOS
         box process. The reason for this is that the method of exiting
         Windows used in Windows v.3.1 and v.3.11 can result in a
         program environment that is lacking CD-ROM drivers.
 
         The performance of C&C in a Windows 95 DOS box is slightly
         slower than in a real DOS environment. You can improve movie
         playback performance by going into the Settings option on
         the Win95 START menu, selecting CONTROL PANEL, then SYSTEM,
         PERFORMANCE, FILE SYSTEM and then CD-ROM. There is a menu
         here which allows you to enable read-ahead buffering of the
         CD (this seems to be disabled by default). Select the setting
         that matches your CD-ROM drive (2X, 4X etc.). You can also
         change the size of the buffer, usually the bigger this is
         the better the performance will be, although this does take
         away memory from the rest of the system.
 
         Autodetecting Soundcards in a Windows 95 DOS box:
 
         Because the Windows 95 DOS box is really just emulating
         DOS (Windows continues to run in the background) you may
         experience problems autodetecting your sound card in this
         mode. There are two things you can do to address this:
 
         1. Do not autodetect, but pick your soundcard manually and
            enter the correct PORT, DMA and IRQ settings, or
         2. Run through Windows 95 DOS mode, as detailed below.
 
         Running through Windows 95 DOS:
 
         If you can choose REBOOT AS MSDOS from the START/SHUTDOWN
         menu and then still access your CD-ROM drive in that mode,
         we recommend running in that environment and installing from
         the DOS prompt. Whether you can do this or not depends on
         having the correct drivers loaded in the DOS environment.
 
 4. Keyboard Shortcuts and Special Features
 ==========================================
 
 C&C has a range of keyboard shortcuts and extra features which are
 keyboard driven. These are intended for the advanced player and are
 not essential to normal gameplay. They are, however, very cool:
 
 Unit Control:
 
 G        : Guard Area
            Select a group of units and then hit G to put them into Guard
            Area mode. In this mode, units will patrol and open fire on any
            enemy units that come within range.

 X        : Scatter Units
            This causes a selected group of units to scatter (for example,
            to make themselves into more difficult targets).

 S        : Stop Unit
            Causes a unit to stop in its tracks.
 
 Keyboard Shortcuts:
 
 F7-F10   : Map Bookmark System
            Use CTRL+F7-F10 to place a bookmark, then use F7-F10 to jump to
            that spot.

 <CTRL>-# : Team Creation
            Use CTRL and a number key (0-9) to mark a group of selected
            units as a team.

 0-9      : Team Selection
            Selects a pre-marked team (see Team Creation) as the 
            current active group.

 TAB      : Open/Close Sidebar
 
 H        : Automatically selects and centers the view around your
            construction yard.
     
 N        : Your next unit on the playing field is selected and the 
            view is centered about it.
          
 R        : Allows resigning in single player mode as well as multiplayer.     

 <HOME>   : Centers the view around the currently selected object.
     
 <ALT>-#  : If the <ALT> key is held while pressing a team number, the
            specified team will be selected and the view centered over
            the team members. This is identical to pressing the team
            number and then pressing <HOME>.

 Multiplayer Options:
 
 A        : Alliance
            Select an enemy unit and hit A. This causes your units to treat
            all the units of the allied side as friendly, as such you will
            not be able to target them. Note that this is not a reciprocal
            arrangement and your new ally must explicitly do the same thing
            to your units. This is a toggle and hitting A for a second time
            will cause you to declare war on your old ally.

 R        : Resign from Multiplayer Game
            If all hope is lost you can resign, or surrender, by hitting the
            R key. This causes all your units to explode in a spectacular
            manner, thus depriving your enemy of absolute victory! It should
            be noted that anyone using this option in other than hopeless
            situations will be considered a wimp by their opponents and
            will be endlessly taunted in subsequent games. Probably.
 
 Cursor Modifiers:
 
 CTRL     : Force Attack
            Holding down the CTRL key forces your cursor into the target
            cursor. This allows you to target your own units, amongst
            other things.

 ALT      : Force Move
            Forces your units to move when they would normally just stand
            and fight. This is useful with tanks against enemy infantry,
            for example. Try it and see.

 CTRL+ALT : Guard Area or Unit
            Select a group of units and then CTRL+ALT click on a building,
            this forces your units to patrol the area around the building
            looking for the enemy. They will engage the enemy if found. If
            you CTRL+ALT click on another one of your units (for example,
            the harvester) your selected units will guard that unit as it
            moves around the map. This also applies to enemy units, which
            is perhaps not so useful.
 
 5. Modem Play Hints
 ===================
 
         Modem Init. Strings
         -------------------
         As detailed in the manual, we seem to get best modem
         performance with modem data-compression and error-correction
         turned off. You can do this by going to the serial game
         settings dialog and entering the appropriate init. string
         for your modem. This should be entered on the host (dialing)
         machine, the guest (receiver) should use ATZ. If you use these
         init. strings the modem speed may have to be set to the exact
         speed of your modem, for example 14000 bps or 28800 bps. Here
         are example init. strings for some popular modems:
 
         Modem                                        Init. String
                                              
         US ROBOTICS SPORTSTER 9600/14400/28800 . . . AT&M0&K0
         DIGICOM SCOUT 288VFCi  . . . . . . . . . . . AT\N1
         BEST DATA SMART ONE 14400  . . . . . . . . . AT\N1
         HAYES ACCURA 28800 . . . . . . . . . . . . . AT&Q0
         SUPRA 14400  . . . . . . . . . . . . . . . . AT\N1
         PRACTICAL 14400  . . . . . . . . . . . . . . AT&Q0
         ZOOM 28800 . . . . . . . . . . . . . . . . . AT&Q0

         Modem Performance Hints
         -----------------------
         With music playing during a modem game, there is a possibility
         of pausing or very slow game play. For optimum performance, 
         music volume under the options menu should be set to zero 
         (far left), this is the default setting. The game speed should
         be satisfactory with sound effects on and music turned down.
 
         486 Machines With External Modems
         ---------------------------------
         If you have a 486 system with an external modem you might
         experience pausing or very slow game play. This is due to
         the 8250 UART chip which is in most 486 class machines, this
         chip causes the CPU to work harder in null modem and modem
         games. There are several work-arounds: 
         
         1. Turn off both music and sound effects in the setup program 
         prior to playing the game. This will improves performance at
         the expense of losing all game sounds. 
         
         2. Install an internal modem. These modems have their own
         UART chips which are designed for higher performance.
 
         3. Install a high performance serial card in your system.
         If you are using a 14400/28800 bps external modem with 
         your 486 class system you should seriously consider installing
         a high performance serial card. These cards usually have a 
         16550A type UART chip which outperforms the 8250 UART in all 
         serial communications applications by buffering data more
         efficiently. 

 6. Network Play Hints
 =====================
 
         General
         -------
         For multiplayer network games we strongly caution you to use a
         homogeneous network environment - that is, to use the same type 
         of IPX compliant network drivers (e.g., IPX, IPXODI etc.) on each
         system. We have found incompatibilities between drivers from
         different manufacturers so you should bear this in mind if you
         are having network game troubles.
 
         MSIPX.COM
         ---------
         C&C should work with any IPX compliant network but we have found
         problems running with Microsoft MSIPX.COM. We strongly recommend
         that you avoid MSIPX and use either IPX.COM from Novell, or use
         IPXODI drivers compatible with your card. If in doubt you should
         ask your network administrator to upgrade your system.

 7. Multi-CD machines and CD-changers
 ====================================

 C&C does not support multiple CD-ROM drives or CD-changers and assumes
 that you only have one CD-ROM drive. If you have more than one CD-ROM
 drive, you should insert the C&C CD you are using into the first CD
 driver letter. For example, if you have drives E:, F: and G:, your
 C&C CD should be inserted into the E: drive.
                     
 8. Game updates and patches
 ===========================

 If it becomes necessary to update your game, you can find game updates 
 on our web page at http://www.westwood.com or at our FTP site 
 (ftp.westwood.com). Please mail all questions to our internet mailing 
 address: mail@westwood.com
