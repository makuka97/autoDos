Various and Sundry System Shock Technical Notes

IMPORTANT NOTE: although the Enhanced CD version of SSHOCK should allow you
to continue save games started in the floppy version, we STRONGLY suggest you 
start over.  Although there have been no radical changes, small details have
changed in various levels, as well as a few small new features and such
which you will not see if you continue an old floppy save game.

1. Pressing the "Print Screen" key will take a screenshot of your current
game and generate a .GIF file in your sshock\gen directory (or in general,
the gen subdirectory of wherever you installed the game).  These GIFs will
be sequentially numbered.

2. Your saved games are stored in your sshock\data directory (or a
subdirectory of whatever directory you installed the game to).  These
eight files are called savgam00.dat, savgam01.dat, ... savgam07.dat.

3. The CD contains both the Enhanced CD version of the game (CDSHOCK.EXE),
which requires 8 Megs of memory to play, and a minor upgrade of the
original floppy version of the game (SSHOCK.EXE), which only requires 4
Megs to play.  CDSHOCK adds audiologs, SVGA cutscenes, prototypical headset
support, and SVGA game play.

4. SSHOCK.EXE contains 128x128 texture maps as well as 64x64.  On a
machine with under 4 1/2Mb free at startup, there will not be room to load
the 128's, and the game will automatically load only the low res maps and
use them.  While this will work fine, you will get grainier, more
pixelated textures.  Thus, if you have an 8Mb machine but are running a
3Mb disk cache, you will be getting low res textures since there will not
be room for the high-res ones.  Also, with even more available memory, you
will have better internal cache performance, and creature bitmaps will be
blended so they will look better at close range.  CDSHOCK.EXE always uses
the 128x128 texture maps.

5. CDSHOCK.EXE allows the game to be played in one of several
high-resolution SVGA modes.  Please note that we have added video modes
large enough that even the best of today's machines will have a hard time
keeping up the pace.  If you are finding the performance in higher
resolution modes to be unplayable, try switching to small-screen view or
try a lower resolution screen mode.

6. Speaking of memory, the game runs under the dos4gw pro 1.97 dos
extender.  At startup it can grab memory from low mem, emm and xms,
depending on the exact memory managers you are running.  If you are
running Qemm, for instance, it can use all free memory.  Under some
versions of EMM386, only some of the high memory is available to the 
extender.  In a brighter future, memory will not be so complicated 
and frustrating.

7. As you probably know, sound card manufacturers have not yet decided on
certain industry standards.  As much as we wanted to fully support all
possible sound cards, we also wanted to ship this game before the chaos
that will no doubt accompany the turn of the century.  As a result, you
should note the following:

  a) ProAudio Spectrum must be run in SoundBlaster Emulation Mode.  We did
  not get working drivers for the PAS.
 
  b) Many SB16-style cards, such as the Fusion-16, the Gateway2000K, and
  so on, are not compatible with the SB16 mixer detection/DMA transfers we
  use in our digital sound system.  Therefore, if you have one of these
  cards, you will have to do one of the following:
     i) Run in SoundBlaster mode.  This will work fine, although you will
  get 2op voices, fewer midi channels, and a reduction in overall sound
  quality.
    ii) Run as a SoundBlaster pro.  
   iii) Try running as a SB16.  Something will happen.  The possiblities
  include it just working (yea!), music working but digital effects not
  panning or volume attenuating, or nothing working at all.
  
  c) In creating the System Shock Enhanced CD, we switched to a new, 
  multi-channel stereo sound system called AIL3. Sadly, the Gravis drivers 
  for this system are not yet complete. We want to support the Gravis 
  Ultrasound in conjunction with AIL3, though, and when the associated Gravis 
  stereo drivers are ready, a patch will be made available.

  d) The installer will try to play a test sample for both sound and midi. 
  If you don't hear any sound, but the installer claims that it was
  successful, try setting it up differently.  If the tests don't produce
  sound, the game probably won't either.
  
8. Hardware Compatibilty Issues:
  As the number of available cards and peripherals continues to increase,
it seems that many "compatible" products are not quite.  Here are some
problems we have encountered, and potential work arounds (or not).
  a) Colorado Spectrum's Notebook Gameport.  This device allows a joystick
to attach to a laptop (or other machine) through a serial cable.  However,
the code to detect it causes certain ACER architecture machines to hang. 
The installer has an "Other Option" page choice for notebook gameport,
which should be set to "Don't Check" by default.  If you turn it on, and
then running the game causes the screen to go black and the machine to
hang, disable it and try running again.  No one has been able to explain
quite what is going on in this case, but the workaround should be fine.
  b) STB Express PCI video cards and the palette.  This now discontinued
PCI card used an Advanced Logic Chipset, and seems to have problems
setting the palette when moderate frequency interrupts (such as used in a
digital mixing environment) are active.  As we have such an environment,
the palette will usually be random if you have digital sound active.

9. System Shock may have problems if your BUFFERS or FILES are set to less
than 30 in your config.sys.  If you are having unexplainable difficulties,
try modifying those lines in your config.sys to support a larger number.

10. If you are still having problems, you can call Origin Technical Support 
at (512) 335-0440, Mon-Fri 9AM-12PM and 1PM-5PM Central Time.

11. Don't waste your magpulse ammo.
  
                                thanks and enjoy,
                                        - The System Shock Team 
                                          Looking Glass










Notes techniques diverses sur System Shock

IMPORTANT: bien que la version CD de SSHOCK devrait vous permettre de 
continuer des jeux sauv‚s commenc‚s sur la version sur disquette, nous 
vous recommendons FORTEMENT de recommencer au d‚but. Mˆme s'il n'y a pas 
eu de changement radical, des petits d‚tails ont chang‚ dans les diff‚rents 
niveaux. De nouvelles caract‚ristiques ont ‚t‚ ajout‚es et vous ne pourrez 
pas les voir si vous continuez … jouer sur les jeux sauv‚s de la disquette 
originale.

1. Appuyer sur "Impr ‚cran" vous permettra d'avoir une vue de l'‚cran
de votre jeu actuel et g‚n‚rera un fichier .GIF dans votre r‚pertoire
sshock\gen (ou en g‚n‚ral, dans le sous-r‚pertoire o— vous avez install‚ 
le jeu).  Ces GIF seront num‚rot‚s par s‚quence.

2. Vos jeux sauv‚s sont enregistr‚s dans votre r‚pertoire sshock\data 
(ou dans le sous-r‚pertoire o— vous avez install‚ votre jeu). Ces huit
fichiers sont appel‚s savgam00.dat, savgam01.dat, ... savgam07.dat.

3. Le CD contient la version CD du jeu (CDSHOCK.EXE), qui n‚cessite
8 Megs de m‚moire pour pouvoir jouer, et une l‚gŠre sophistication de
la version originale sur disquette (SSHOCK.EXE), qui n‚cessite uniquement
4 Megs pour jouer. Dans le CDSHOCK, il y a aussi des audiologs, des cutscenes
SVGA, un prototype de casque, et un jeu SVGA.

4. SSHOCK.EXE contient des cartes de texture 128x128 ainsi que des 64x64.  
Sur une machine qui a moins de 4 1/2Mb au d‚marrage, il n'y aura pas de
place pour charger les 128, et le jeu chargera automatiquement et uniquement
les cartes de faibles r‚solutions afin de les utiliser. Si cela se passe
bien, vous aurez des textures plus granuleuses et plus farfelues. Cependant,
si vous avez un ordinateur 8Mb avec un disque cache de 3Mb, vous aurez des 
textures de faible r‚solution, car il n'y aura pas assez de place pour
celles … forte r‚solution. Aussi, avec plus de m‚moire, vous obtiendrez
une performance cache interne meilleure, les mappes binaires se 
m‚langeront mieux et seront ainsi de meilleure qualit‚.  CDSHOCK.EXE 
utilise toujours les cartes de texture 128x128.

5. CDSHOCK.EXE permet de jouer dans un des modes SVGA … forte r‚solution. 
Faites attention, car nous avons ajout‚ des modes vid‚o si grands
que mˆme les machines les plus perfectionn‚es auront du mal … soutenir
le rythme. S'il vous est difficile de jouer avec ces modes … forte 
r‚solution, essayez de revenir … une vue ‚cran plus petite ou bien 
essayez un mode … faible r‚solution.

6. A propos de m‚moire, le jeu est lanc‚ … partir du prolongateur dos 
dos4gw pro 1.97. Au d‚marrage, il peut soutirer de la m‚moire de 
low mem, emm et xms, selon les gestionnaires de m‚moire que vous
poss‚dez. Si vous utilisez Qemm, par exemple, il peut utiliser toute
la m‚moire disponible. Avec les versions de EMM386, seule une partie
du haut de m‚moire est disponible au prolongateur. Dans un futur
meilleur, la m‚moire ne sera plus aussi compliqu‚e et aussi frustrante.

7. Comme vous le savez certainement, les fabriquants de carte son
n'ont pas encore d‚cid‚ des standards de l'industrie. Mˆme avec toute
notre bonne volont‚ en ce qui concerne les cartes son sur le march‚, 
nous voulions sortir ce jeu avant le chaos qui attend la fin de ce siŠcle.
Prenez en compte les informations suivantes:

  a) ProAudio Spectrum doit ˆtre utilis‚e avec un mode Emulation SoundBlaster. 
  Nous n'avons pas pu faire fonctionner les gestionnaires pour le PAS.
 
  b) Beaucoup de cartes de style SB16, comme la Fusion-16, la Gateway2000K 
  etc... ne sont pas compatibles avec les transferts SB16 m‚langeur 
  d‚tection/DMA que nous utilisons dans notre systŠme de son digital. Ainsi, 
  si vous avez une de ces cartes, vous devrez faire une des choses suivantes:
     i) Utiliser un mode SoundBlaster. Ceci fonctionnera, malgr‚ des voix
  2op, quelques canaux midi et une baisse de qualit‚ g‚n‚rale du son.
    ii) Utiliser comme un SoundBlaster pro.  
   iii) Essayer d'utiliser comme une SB16. Quelque chose va se produire.  
  Les possibilit‚s incluent un bon fonctionnement (youpi!), une musique 
  qui fonctionne mais des effets digitaux panoramiques ou un volume
  att‚nu‚, ou bien un ‚chec total du fonctionnement.
  
  c) En cr‚ant cette version am‚lior‚e de System Shock CD, nous avons cr‚‚
  un nouveau son st‚r‚o … canaux mutiples appell‚ AIL3. Malheureusement,
  les gestionnaires Gravis sont encore incomplets. Nous supportons le 
  Gravis Ultrasound en conjonction avec AIL3, et quand les gestionnaires
  st‚r‚o associ‚s avec Gravis seront prˆts, nous vous procurerons un 
  "patch".
  
  d) Vous ferez une tentative de jeu avec le son et midi. 
  Si vous n'entendez rien, et que l'installer continue … afficher une
  installation r‚ussie, essayez de le r‚gler diff‚remment. S'il n'y a
  pas de son durant les tests, il n'y en aura probablement pas durant le
  jeu.

8. Solutions pour la compatibilit‚ du mat‚riel:
  Le nombre de cartes disponibles et de p‚riph‚riques continuent
  d'augmenter, mais pas le nombre de produits "compatibles". Voici 
  quelques problŠmes dont nous nous sommes aper‡us, et quelques
  tuyaux (ou rien).
  a) Port Jeu Carnet Colorado Spectrum. Ce p‚riph‚rique permet … un 
joystick de s'attacher … un ordinateur portable (ou … un autre ordinateur)
avec un cable de s‚rie. Cependant, le code pour le d‚tecter peut bloquer
certains ordinateurs … architecture ACER. L'installer a un choix de page
"Autre Option" pour le port jeu du carnet, qui devrait ˆtre r‚gl‚ par 
d‚faut sur "Ne pas v‚rifier". Si vous l'avez programm‚ ainsi, et que le 
fait de lancer le jeu rend l'‚cran noir ou bloque l'ordinateur, mettez-le
hors service et essayez de relancer. Personne, jusqu'… pr‚sent, n'a ‚t‚ 
capable d'expliquer cela, mais le tuyau devrait fonctionner.
  b) Cartes vid‚o STB Express PCI et la palette: Cette carte PCI, aujourd'hui 
en rupture de production, et cette Puce Logique Avanc‚e semblent avoir des  
problŠmes avec les r‚glages de la palette quand des interruptions de 
fr‚quence mod‚r‚es (comme par exemple celles utilis‚es dans un environnement
de mixage digital) sont en place. Comme nous avons ce genre d'environnement, 
la palette sera hasardeuse si vous avez un son digital en place.

9. Vous pouvez avoir des problŠmes avec System Shock si vos TAMPONS ou vos 
FICHIERS sont r‚gl‚s … moins de 30 dans votre config.sys. Si vous ne
comprenez pas ce qui se passe, essayez de modifier ces lignes dans votre
config.sys afin qu'elles puissent contenir un plus grand nombre.

10. Si vous avez encore des problŠmes, vous pouvez appeler le Service
ClientŠle Technique de Origin au (512) 335-0440, du lundi au vendredi
entre 9AM-12PM et 1PM-5PM, heure locale.

11. Ne gƒchez pas vos munitions de magpulse.
  
                                Merci et amusez-vous bien,
                                        - L'‚quipe de System Shock, 
                                          Looking Glass









Diverse technische Hinweise zu System Shock
WICHTIG: Obwohl die CD-Version von SYSTEM SHOCK es Ihnen erlauben sollte,
in der Floppy-Version begonnene Spiele fortzusetzen, raten wir DRINGEND, 
von vorne anzufangen. Obwohl das Spiel nicht radikal ge„ndert wurde, 
gibt es doch verschiedene Detail„nderungen, zudem wurden einige neue Elemente 
hinzugefgt, die Sie nicht sehen werden, wenn Sie mit dem
Spiel aus der Floppy-Version weiterspielen.

1. Wenn Sie die Taste "Druck" bet„tigen, macht dies eine Aufnahme
Ihres jetzigen Bildschirms und erzeugt eine .GIF-Datei in Ihrem 
sshock\gen Verzeichnis (oder allgemein in dem Gen-Unterverzeichnis
Ihres Speicherverzeichnisses). Diese GIFs werden der Reihe nach
durchnumeriert.

2. Ihre Spiele werden im Verzeichnis sshock\data abgespeichert (oder
einem Unterverzeichnis des jeweiligen Verzeichnisses, in dem Sie 
das Spiel installiert haben). Diese acht Dateien heiáen
savgam00.dat, savgam01.dat, ... savgam07.dat.

3. Die CD enth„lt sowohl die verbesserte CD-Version des Spiels (CDSHOCK.EXE),
die 8 Megabyte Speicher ben”tigt, als auch eine leicht ver„nderte Version
der ursprnglichen Floppyversion das Spiels (SSHOCK.EXE), die nur 4
Megabyte ben”tigt.  CDSHOCK hat Audiologs, SVGA Cutscenes, teilweise
Cyberhelm-Untersttzung, und SVGA-Spielszenen.

4. SSHOCK.EXE enth„lt sowohl 128x128 Texturen als auch 64x64.  Auf einer
Maschine, die beim Start weniger als 4 1/2Mb frei hat, ist nicht genug Platz 
fr die 128er, und das Spiel l„dt automatisch nur die niedrigaufl”senden 
Texturen. Diese Version funktioniert zwar, aber Sie sehen gr”bere,
unsch„rfere Texturen. Wenn Sie also eine 8-Mb Maschine haben, aber
3Mb als Cache benutzen, sehen Sie die niedrigaufl”senden Texturen, 
da Sie nicht genug Speicher fr die hochaufl”senden haben.
Auáerdem fhrt noch mehr Speicher zu einer Leistungsverbesserung,
die interne Cache funktioniert besser, und die dargestellten
Wesen sehen sogar aus der N„he sehr scharf aus.  CDSHOCK.EXE benutzt immer
die 128x128 Texturen.

5. CDSHOCK.EXE l„át Sie zwischen mehreren hochaufl”senden
SVGA-Standards w„hlen.  Denken Sie bitte daran, daá wir 
so umfangreiche Videostandards hinzugefgt haben, daá sogar die 
besten heutigen Maschinen nur schwer mithalten k”nnen.
Falls die Leistung Ihres Computers in den hochaufl”senden Standards 
zu gering ist, schalten Sie doch auf den kleinen Bildschirm um,
oder versuchen Sie einen Modus mit geringerer Aufl”sung.

6. Weil gerade vom Speicherplatz die Rede war, das Spiel 
l„uft untder dem Programm dos4gw pro 1.97 dos
extender. Beim Start kann es Speicherplatz vom niedrigen,
Speicherbereich, EMM und XMS an sich ziehen, je nachdem, welchen
Speichermanager Sie benutzen.  Falls Sie beispielsweise
QEMM benutzen, kann es allen freien Speicher verwenden.
Bei manchen Versionen von EMM386, ist nur ein Teil des hohen 
Speicherbereichs fr den extender verfgbar. Eines Tages
wird hoffentlich das Problem des Speichers nicht mehr so kompliziert 
und frustrierend sein.

7. Wie Sie wahrscheinlich wissen, haben sich die Hersteller von
Soundkarten noch nicht auf industrieweite Standards einigen k”nnen.
Wir wrden ja gerne alle erh„ltlichen Soundkarten untersttzen,
aber wir wollten auch das Spiel vor der Jahrtausendwende
ausliefern. Deshalb sollten Sie Folgendes beachten:

  a) ProAudio Spectrum muá im SoundBlaster-Emulationsmodus laufen.  Wir haben
  keine funktionierenden Treiber fr die PAS erhalten.
 
  b) Viele SB16-artigen Karten, so etwa die Fusion-16, die Gateway2000K, usw.
  sind nicht mit den SB16 Mixer Detection/DMA Transfers kompatibel, die wir
  in unserem digitalen Soundsystem verwenden. Deshalb sollten Sie dann
  eine der folgenden  Optionen w„hlen:
  
     i) SoundBlaster-Modus w„hlen.  Dies funktioniert, obwohl Sie dann
  2op-Stimmen, weniger Midi-Kan„le, und eine allgemein geringere
  Tonqualit„t haben.
    ii) Als SoundBlaster Pro laufen lassen.  
   iii) Als SB16 laufen lassen.  Was passieren kann ist, daá es
  gerade so funktioniert (yea!), daá die Musik funktioniert, aber 
  nicht die digitalen Effekte, daá die Lautst„rke absinkt, oder daá gar
  nichts funktioniert.
  
  c) Wir haben fr die System Shock CD-Version ein neuartiges 
  Multikanal-Stereosoundsystem namens AIL3 benutzt. Leider sind die 
  Gravis-Treiber fr dieses System noch unvollst„ndig. Wir wollen
  jedoch die Gravis Ultrasound in Kombination mit AIL3 untersttzen. 
  Sobald wir die notwendigen Gravis Stereo-Treiber erhalten, 
  werden wir unseren Kunden ein Zusatzprogramm zur Verfgung stellen, 
  um dieses Problem zu beheben.
   
  
  d) Das Installationsprogramm wird versuchen, sowohl fr Sound als
  auch MIDI einen Test abzuspielen. Wenn Sie nichts h”ren, aber das
  Installationsprogramm den Test als gelungen ansieht, „ndern Sie 
  bitte die Einstellungen. Wenn der Test keinen Ton hervorbringt,
  trifft das wahrscheinlich auch auf das Spiel zu.

8. Hardware-Kompatibilit„t:
  Da die Anzahl der angebotenen Karten und Peripheriger„ten dauernd
  ansteigt, sieht es so aus, als ob viele "kompatible" Produkte
  nicht ganz kompatibel sind. Es folgen einige von uns entdeckte  
  Probleme und m”gliche L”sungen (oder auch nicht):
  a) Colorado Spectrum's Notebook Gameport.  Dieses Ger„t l„át Sie mit
  Hilfe eines seriellen Kabels einen Joystick an ein Laptop (oder einen
  anderen Computer) anschlieáen.  Allerdings fhrt sein Code bei manchen,
 ACER Maschinen zum Absturz. Das Installationsprogramm hat einen
 Menpunkt "Andere Optionen" fr den Notebook Gameport, der standardm„áig auf
 "Nicht Testen" eingestellt sein sollte.  Wenn Sie dies „ndern, und
dann w„hrend des Spiels der Bildschirm dunkel wird und das
Spiel h„ngt, gehen Sie zur Standardeinstellung zurck und versuchen 
Sie's noch einmal. Es ist unbekannt, was da passiert, aber die
L”sung hat sich bew„hrt.

  b) STB Express PCI Videokarten und die Palette.  Diese inzwischen nicht mehr
  erh„ltliche PCI-Karte benutzte einen Advanced Logic Chipsatz 
  und schien Probleme mit der Palette zu haben, wenn es zu m„áigen
  Frequenzunterbrechungen kam (wie etwa beim digitalen Mischen). Da dies
  in unserem Spield er Fall ist, wird die Palette instabil sein, wenn
  der digitale Sound aktiviert ist.

9. System Shock kann Probleme haben, wenn BUFFERS oder FILES in der 
config.sys-Datei auf weniger als 30 eingestellt sind.  Falls Sie
nicht erkl„rbare Probleme haben, versuchen Sie doch, diese Zeilen
in Ihrer config.sys  auf einen h”heren Wert einzustellen.

10. Sollten Sie immer noch Probleme haben, k”nnen Sie den Origin Kundendienst 
unter der Nummer (512) 335-0440, Mo-Fr von 9-12 und 13-17h 
(Central Time) erreichen.

11. Verschwenden Sie nicht Ihre Magpuls-Munition.
  
                                Vielen Dank und Viel Spaá,
                                        - Das System Shock Team 
                                          Looking Glass
