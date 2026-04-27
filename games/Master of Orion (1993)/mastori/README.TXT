--=={[ M A S T E R   O F   O R I O N ]}==--

Thank you for buying Master of Orion. The following text is provided 
as an addition to your manual and technical suppliment.

README.TXT CONTENTS:
--------------------        
- Technical Notes
- Version 1.3 Changes
- Quick Start Questions and Answers
     
     

     ********************* TECHNICAL NOTES *********************


- NOTE: You can't run save games from version 1. You must start
        a new game. You can run save games from version 1.2.

- Make sure that you have at least 570K conventional, and 1040K of 
  expanded memory. Use the DOS command MEM to determine if you have 
  enough conventional and expanded memory.

- If you receive a "reconfigure hardware" error message when trying
  to run Master of Orion, check your sound card settings. You must
  have the correct ADDRESS, IRQ, and DMA settings. Also, make sure
  that you don't have programs in memory that may conflict with your
  sound card settings.

- The Install program's sound card detection routines may cause some
  systems to lock up right after sucessfully installing the game. If 
  this happens to you, run the Install program by typing 
  "INSTALL -S" instead of just "INSTALL". This bypasses the 
  auto-detection, and lets you select any sound card on the menu.

- Sound Blaster Pro Cards should have all environment variables 
  (specifically the BLASTER variable) fully specified in the 
  config.sys file to be properly recognized.

- Roland sound cards take several seconds to load custom instrument 
  files at the beginning of the program, when switching to and from 
  the main menu, and at the end of the game.

- Adaptec controller cards must use the hard drive drivers supplied 
  with the controller cards to access the game properly.

- The program automatically saves your game in a special file that 
  allows you to Continue where you left.  However, if you fail the 
  ship identification security check, this file is deleted and the 
  Continue function is disabled.

- If you are using Stacker, Double Space, or some other hard drive 
  compression utility, "Master of Orion" will appear to use more 
  than the amount of space the Install utility checks for. This is 
  because the program files are already compressed, and your 
  compress utility will not be able to get the usual space savings.
     ******************** VERSION 1.3 CHANGES ******************

-NEW KEY CONTROLS     

F1 - Help
F2-  Cycle to next colony
F3-  Cycle to previous colony
F4-  Cycle to next newly created fleet
F5-  Cycle to previous newly created fleet
F6-  Cycle to next fleet
F7-  Cycle to previous fleet
F8-  Cycle to next colony that has enemy ships enroute
F9-  Cycle to previous colony that has enemy ships enroute
F10- Instantly saves game to Continue Game File

The F8 and F9 keys require Advanced Scanner tech.
     
1. Pressing ALT-P will change all emperor personalities at random.

2. Tech Screen: '=' sets all research allocations to the same 
   amount.

3. You can toggle random events off and on by holding the ALT key 
   down and typing 'EVENTS'.

4. ALT-M will display a 5 parsec by 5 parsec grid on the control 
   screen.

5. The "C" key will tell you how many spies were caught that turn.

6. The "B" key will allow you to scrap missile bases.

7. ALT-C centers the screen on the current planet.

8. ALT-R changes all RELOCation destinations to the selected 
    planet.

- DIPLOMACY CHANGES

1. If you ask another race to break an alliance or declare war, they 
   are more likely to request a technology tribute.

2. High Council Votes: another race voting for you no longer creates 
   an automatic alliance. Instead, voting for a candidate improves 
   your relationship with them, and hurts the relationship with the 
   other candidate. Abstaining slightly harms relationships with 
   both candidates.

3. You can now offer tech tribute if you have no planetary reserve.

4. Allies that have lost contact will not appear until contact is 
   reestablished.

5. Committing genocide penalizes all diplomatic relations.

- INFORMATION DISPLAYS

1. Race Status screen highlights technology you do not have.

2. If you have Improved or Advanced Scanners, red lines on the main 
   galaxy map will show enemy ships approaching the current star 
   system being viewed (F7 and F8 keys).

3. Stargates are shown on the main screen.

4. Colony flags are shown on MAP screen in all three modes.

5. MAP screen frames portion of galaxy in Main view.

6. Instructions displayed for TRANS and RELOC buttons are worded 
   more clearly.

7. Eliminated races no longer appear in STATUS screen.

- COMBAT AI

1. Ships retreat away from enemies, not just left or right.

2. Ships with Warp Dissipators do not continue firing them at 
   immobilized targets.

3. Ships avoid friendly ships with Pulsar weapons.

4. Ships with long range beams now close to range of 1 when 
   attacking planets.

5. Ships do not fire missiles if target ships could back out of 
   range.

6. First salvo of planetary missiles correctly uses scatter pack or 
   single shot type.

7. AUTO combat runs faster.

- GENERAL AI

1. Improvements in estimating size of attack fleets needed for 
   assaults.

2. Colony ships will usually travel with armed escorts.

3. When player's ships have Warp Dissipators, AI will compensate in 
   new ship designs.

- COSMETIC CHANGES

1. End Game Victory - Emperor's robes changed.

2. V1.3 and copyright notice on main menu screen.

- FUNCTIONAL CHANGES

1. Enemies can no longer use your stargates.

2. Repulsor beams end movement for ships they are used against.

3. Discovering any Artifact planet gives you a chance to find new 
   tech.

4. When discovering technologies that request a resource allocation 
   change (terraforming, robotic controls, planetary shields, etc.), 
   the ALL button has been changed to a 75% button.  Also, it only 
   requests changes if the new tech is superior to your existing 
   tech.

5. If you want to DESIGN when you have six ships in play, you do not 
   have to SCRAP until after the design is done.

6. Ships that have been given orders but are still in orbit (on the 
   left side of the planet) can now be selected and have their 
   orders changed. They can also be ordered to stay at the home 
   planet by selecting the planet as destination.

7. Fertile and Gaia planets increase your planets' base populations
   by 25% and 50% respectively, in addition to the increased growth 
   rates.

8. If you have both standard and scatter pack missiles, you may 
   change which type your planetary bases fire by using the 
   MISSILES button in combat.  In Auto-Combat mode, the computer 
   automatically selects the more effective type.

9. The High Council is formed when 2/3rds of the planets have been 
   colonized, not 1/2 as stated in the manual.

- INTERNAL CHANGES

1. Stargates cost 3000 not 350

2. Crystal & Ameoba kill pirates now.

3. Cost of colony bases fixed. 

4. Displacer Device costs corrected

5. Text for zeon missiles corrected.

6. Less likely to start game in a bad position at harder levels.  

7. Research rolls now guarantee a selection of some key technologies 
   such as missiles.

8. Missile Bases are slightly cheaper, about .6 of a large ship.
 
9. Fleet sizes over 32,000 are no longer shown as negative.

10. A vote of exactly 2/3rds in council wins.

Changes to Weapons Reference Tables:
Power for Lasers is now 25.  
Heavy Lasers 75.  
Maulers 300.  
Auto-Blaster 90.
Power for all Bombs and Biologicals is now 10.
Scatter Pack V has power rating of 50.

Sizes have changed on the following Weapons:
Nuclear Bombs   40
Fusion Bombs    50
Death Spores            100
Anti-Matter             75
Omega V         140
Doom Virus              200
Neutronium Bomb 200
Bio Terminator  300 
Scatter Pack VII        170



QUICK START QUESTIONS AND ANSWERS

If you are familiar with mouse-based interfaces, and want to leap 
immediately into the game without reading the manual, the following 
answers cover many of the basic "how to" concepts you'll need to 
play Master of Orion.

How do I send my ships to another planet?
Select one of your ship icons in orbit around a planet.  The right 
panel will display which ships are in orbit around that world.  Use 
the arrow buttons by each ship type to change the number of ships 
you will send.  Choose a destination planet for your fleet, then 
select the ACCEPT button.  See page 16 of the manual for more 
information.

How do I create a new colony?
Send a colony ship there (i.e. a ship equipped with a special colony 
base device).  If the planet is habitable (see pages 17-18 of the 
manual), you will automatically be asked if you want to land and 
establish a colony there.  Your colony ship is disassembled and its 
parts used to establish the colony.  Once you have set up your 
colony base, you should immediately transport more colonists to that 
planet, to help it grow more quickly.

How do I TRANSport my colonists to another planet?
Select the planet you wish to transport your people FROM.  Select 
the TRANS button from the panel on the right, then select the planet 
you wish to send your people to.  After you have chosen the 
destination planet, you can use the slider bar on the right panel to 
decide how many people you want to send, up to half the population 
of your source planet.  Note that you cannot send people to a planet 
that has not yet established a colony base, and you cannot transport 
to a planet you have not yet explored.

If you are sending transports to an enemy colony, you do the same 
thing. The people you send to an enemy world are automatically armed 
with the latest technology for ground combat.  Note that enemy ships 
and missile bases can destroy your transports before they can land.  
This combat happens automatically when your transports arrive at 
their target world, and you see only the results.  For more 
information, see pages 20 and 60 of the manual.

Why can't my colony ships travel as far as my scouts do?
Your scouts are equipped with a special device called "Reserve Fuel 
Tanks" that let them travel to planets 3 parsecs farther away than 
your other ships can.  At the start of the game, your scouts can 
reach any star within six parsecs of any of your colonies, but your 
other ships can only reach planets 3 parsecs away.  

Note that when you are moving ships from one planet to another, all 
that matters is how far the destination star is from the nearest 
friendly colony.  Your ships do not actually stop at one of your 
colonies to refuel.  Also, when your scientists discover a new fuel 
type that increases your range, all of your ships immediately 
benefit from the discovery.  You do not need to design new ships to 
use that fuel.  

How do I change the destination of my fleets in space?
At the start of the game, once your ships have left orbit to go to 
another planet, their destination cannot be changed.  If you change 
your mind during the same turn you gave orders, you can select the 
ship icon in orbit at the LEFT of the planet, and direct it to a 
new planet or back to its original planet.  Once you develop 
Hyperspace Communications (34th level Computer Technology), you can 
change the orders of any ships en route to other planets.at any time.

I just signed a Non-Aggression Pact with another race, and he 
attacked my planet the very next turn.  What gives? 
Just like you, the other races cannot change the orders of their ships 
and transports en route.  The attacking forces were probably sent to 
your planet before the pact was signed, and did not know that you 
are now on friendly terms.

I just got the technology for Controlled Barren (or Tundra, 
Inferno, etc.) Landings.  Why can't my colony ships land on those 
planets now?
Once you discover the technology for landing on a hostile planet 
type, you must design a new type of colony ship with the special 
base device for landing on that environment.  However, that new 
type of colony transport can also land on any less hostile planet.  
For instance, a ship equipped to land on inferno planets can also 
colonize dead, tundra, barren, and standard planet types.

How do I conquer an enemy's planet?
You do not need to send a colony ship.  You just transport enough 
people to that planet to defeat the populace there and capture 
their colony.  However, since missile bases and enemy ships in orbit 
can destroy transports before they land, we recommend that you send 
battle fleets to your target planet first, to eliminate any threat 
to your transports.

What does RELOC do?
The RELOC button lets you automatically send the ships that one 
planet builds to another planet.  This is useful to assemble your 
fleets at one common staging point.  To RELOCate your ships' 
destination, select the RELOC button, then select the planet you 
wish to send your completed ships to.  A blue line will appear, 
connecting the worlds. To cancel the RELOCation, select the RELOC 
button, then select the same source planet as the "destination" 
(i.e. relocating your ships to where they started.)

Can I refit my existing ships to use new technologies?
No.  If you wish to equip ships with new technologies, you have to 
design a new class of ship to use them.  If you already have six 
classes in use, you may have to make a tough choice to scrap some 
older ship types to make room for the new design.

What is this Guardian thing that keeps destroying my ships?
Legends hold that the Ancient Ones built terrible automated war 
machines to protect Orion from invaders.  So, if you find a planet 
protected by The Guardian, you have probably found Orion.  Needless 
to say, you will need a large fleet with advanced technology before 
you can defeat the Guardian, and capture Orion.

Why can I research some high level technology, when I did not get a 
choice to discover lower level advances?  For instance, I can 
research "Deuterium Fuel Cells (Range 5)", but I never got to 
choose "Hydrogen Fuel Cells (Range 4)"?
The technologies that your scientists can research are partially 
based on random chance (the muse of scientific inspiration is 
fickle).  If you cannot research a particular device, you may have 
to acquire it through espionage or diplomatic exchange.  You can 
also get new technology by capturing enemy planets, provided that 
you have left some of their factories intact. The more factories, 
the greater chance of finding technology.

Special Thanks:
The Master of Orion team would like to thank the following people 
who provided design suggestions, caught bugs, and otherwise helped 
to polish v1.3 of the game:
Don Aldrich, Gail & Patrick Barnes, Ken Fishkin, Tom Holsinger, 
Tim Jordan, William Kutscher, Marvin Lamb, Kelly McCauley, 
Stephen Mintenko, Jerry Pournelle, and David Weinstein.

********************************************************************

If you have any questions or problems, call the MicroProse Customer 
Service Hotline at (410)771-1151, Monday-Friday, from 9am-5pm EST.

********************************************************************

