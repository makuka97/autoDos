AutoDOS — Windows Edition
A lightweight personal DOS game launcher for Windows, built in Python with tkinter and powered by DOSBox Staging.
Overview
AutoDOS lets you add DOS game archives or pre-extracted game folders to a library and launch them directly into DOSBox with no manual configuration. It handles extraction, executable detection, DOSBox settings, and CD mounting automatically.
Tech Stack

Python 3.12+ — core application
tkinter — native GUI, no external UI dependencies
Pillow — logo rendering
DOSBox Staging 0.82 — DOS emulation backend
7-Zip (7za.exe) — bundled archive extraction
PyInstaller — packages everything into a standalone Windows exe
ExoDOS database — game compatibility data (cycles, memory, settings)

How It Works
Adding games — AutoDOS accepts zipped archives via Add Zip, or pre-extracted folders via Add CD. On ingest it extracts the archive, scans for executables and bat files using a scoring algorithm, applies ExoDOS settings if a match is found, and launches immediately.
Executable detection — A scoring system ranks every exe and bat file found in the game folder. It penalises root-level Windows launcher bats, emulator subfolders, setup and sound utility files, and utility directories like ULTRASND. The highest-scoring file launches automatically. If the result is ambiguous, a picker modal lets you choose manually.
ExoDOS integration — On ingest, the game name is matched against the ExoDOS database using exact key matching, containment matching, and token matching. When a match is found, CPU cycles, memory size, XMS, and EMS settings are applied silently. Unrecognised games default to 3000 cycles and 16MB.
CD support — Games with disc images can have an ISO folder assigned via the Add CD button. AutoDOS sorts the ISOs alphabetically, mounts the first disc as D: in DOSBox, and instructs the user to use Ctrl+F4 inside DOSBox to swap discs when prompted.
Launch — DOSBox is launched via subprocess with per-game cpu_cycles, memsize, and mount commands passed as -c arguments. Memory values are snapped to valid DOSBox values automatically.
Functionality

Add games from ZIP, 7Z, or RAR archives
Add pre-extracted CD-based games directly from folder
Automatic exe and bat detection with intelligent scoring
ExoDOS database lookup with fuzzy matching
Per-game settings — cycles, memory, XMS, EMS, CD path
Live ExoDOS search in game settings for manual tuning
Right-click context menu — change exe, game settings, remove
Multi-disc support with Ctrl+F4 swap instructions
Persistent game library stored in library.json
Standalone exe via PyInstaller — no Python installation required

Credits
Game compatibility data sourced from the ExoDOS collection. DOSBox Staging developed by the DOSBox Staging team.
