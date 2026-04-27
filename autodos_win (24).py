"""AutoDOS — A lightweight personal DOS game launcher."""

import json
import re
import os
import shutil
import subprocess
import tarfile
import threading
import zipfile
from datetime import date
from pathlib import Path
from tkinter import filedialog, messagebox
import tkinter as tk
import tkinter.ttk as ttk

# ── Constants ────────────────────────────────────────────────────────────────
import sys as _sys
# BASE_DIR  = folder where AutoDOS.exe (or autodos_win.py) lives
#             used for: dosbox\, tools\, games\, library.json
# ASSET_DIR = where bundled read-only assets are extracted
#             used for: logo.png, dosbox.conf, master_games.json
if getattr(_sys, "frozen", False):
    BASE_DIR  = Path(_sys.executable).parent
    ASSET_DIR = Path(_sys._MEIPASS)
else:
    BASE_DIR  = Path(__file__).parent
    ASSET_DIR = BASE_DIR
GAMES_DIR       = BASE_DIR / "games"
LIBRARY_FILE    = BASE_DIR / "library.json"
LOGO_FILE       = ASSET_DIR / "logo.png"
ICON_FILE       = ASSET_DIR / "icon.ico"

DOSBOX_BINS     = ["dosbox-staging", "dosbox"]
TOOLS_DIR       = BASE_DIR / "tools"
EXODOS_FILE     = ASSET_DIR / "master_games.json"
DOSBOX_FLATPAK  = "io.github.dosbox-staging"

# Windows bundled paths
DOSBOX_WIN_PATH = BASE_DIR / "dosbox" / "dosbox.exe"
TOOLS_7ZA       = TOOLS_DIR / "7za.exe"
TOOLS_UNRAR     = TOOLS_DIR / "unrar.exe"

BG              = "#f0ece8"
LIST_BG         = "#ffffff"
ALT_ROW_BG      = "#f7f7f7"
SEL_BG          = "#e8f0fe"
BTN_BG          = "#e8e4e0"
BTN_ACTIVE      = "#d4cfc9"
BORDER          = "#d0ccc8"
TEXT            = "#1a1a1a"
MUTED           = "#999999"

SETUP_NAMES     = {"setup", "install", "config", "unins", "uninst", "uninstall"}
LAUNCHER_NAMES  = {"setup.exe", "install.exe", "play.exe", "start.exe", "launch.exe"}

# Default to All Files so user sees everything without switching filters
ARCHIVE_FILTERS = [
    ("All Files", "*.*"),
    ("Archives", "*.zip *.7z *.rar *.tar.gz *.tgz"),
]

# ── CD / ISO Support ──────────────────────────────────────────────────────────
CD_IMAGE_EXTS   = {".iso", ".bin", ".cue", ".img", ".mdf"}
CD_FOLDER_NAMES = {"cd", "cdrom", "cd-rom", "disc", "disk", "dvd",
                   "cd1", "cd2", "disc1", "disc2", "disk1", "disk2"}

_ISO_EXE_BLACKLIST = {
    "setup", "install", "uninst", "uninstall", "patch", "update",
    "config", "cfg", "register", "readme", "read", "help",
    "directx", "dxsetup", "dos4gw", "cwsdpmi", "himemx",
    "dosbox", "scummvm", "loadpats", "intro", "movie", "logo",
    "start", "run", "main", "fixsave", "convert",
}


def detect_cd_source(game_dir: Path) -> list:
    """Scan a game folder for CD images. Returns sorted list of path strings."""
    images = []
    for ext in CD_IMAGE_EXTS:
        images += list(game_dir.rglob(f"*{ext}"))
        images += list(game_dir.rglob(f"*{ext.upper()}"))
    if images:
        return sorted(str(f) for f in set(images))
    for child in game_dir.iterdir():
        if child.is_dir() and child.name.lower() in CD_FOLDER_NAMES:
            found = []
            for ext in CD_IMAGE_EXTS:
                found += list(child.glob(f"*{ext}"))
                found += list(child.glob(f"*{ext.upper()}"))
            if found:
                return sorted(str(f) for f in set(found))
    return []


def scan_iso_for_exes(iso_path: str) -> list:
    """Use 7za to list ISO contents and return all candidate exe names.
    Returns list of uppercase exe filenames e.g. ['WC3.EXE', 'INSTALL.EXE']
    Blacklisted names are filtered out.
    """
    sevenzip = str(TOOLS_7ZA) if TOOLS_7ZA.exists() else shutil.which("7za") or shutil.which("7z")
    if not sevenzip:
        return []
    try:
        result = subprocess.run(
            [sevenzip, "l", iso_path],
            capture_output=True, text=True, timeout=60
        )
        listing = result.stdout
    except Exception:
        return []

    seen = set()
    candidates = []
    for line in listing.splitlines():
        line = line.strip()
        if len(line) < 4:
            continue
        upper = line.upper()
        if not (upper.endswith(".EXE") or upper.endswith(".COM") or upper.endswith(".BAT")):
            continue
        parts = line.split()
        if not parts:
            continue
        fname = parts[-1]
        for sep in ("/", "\\"):
            if sep in fname:
                fname = fname.split(sep)[-1]
        name = fname.upper()
        if not name or name in seen:
            continue
        stem = name.rsplit(".", 1)[0].lower() if "." in name else name.lower()
        if stem in _ISO_EXE_BLACKLIST or len(stem) < 2:
            continue
        seen.add(name)
        candidates.append(name)

    # Sort: EXE first, then BAT, then COM
    def rank(name):
        ext = name.rsplit(".", 1)[-1] if "." in name else ""
        return ({"EXE": 0, "BAT": 1, "COM": 2}.get(ext, 3), name)

    candidates.sort(key=rank)
    return candidates

# ── Helpers ──────────────────────────────────────────────────────────────────

def snap_memsize(mb: int) -> int:
    """Snap a memsize value to the nearest valid DOSBox value (power of 2, max 384)."""
    valid = [1, 2, 4, 8, 16, 32, 64, 128, 256, 384]
    return min(valid, key=lambda x: abs(x - mb))


def find_dosbox() -> tuple | None:
    """Return (binary, prefix_args) for the best DOSBox found, or None."""
    if DOSBOX_WIN_PATH.exists():
        return (str(DOSBOX_WIN_PATH), [])
    for b in DOSBOX_BINS + ["dosbox-staging.exe", "dosbox.exe"]:
        if shutil.which(b):
            return (b, [])
    return None


def load_exodos() -> dict:
    """Load the ExoDOS game database if present."""
    if EXODOS_FILE.exists():
        try:
            return json.loads(EXODOS_FILE.read_text(encoding="utf-8")).get("games", {})
        except Exception:
            pass
    return {}


def exodos_key(name: str) -> str:
    """Normalize a game name to an ExoDOS lookup key.
    Strips common noise words found in zip filenames (dos, win, gog, years etc.)
    """
    import re
    noise = r"\b(dos|win|windows|gog|cd|cdrom|version|v\d+|19\d\d|20\d\d)\b"
    cleaned = re.sub(noise, "", name.lower())
    # Strip all non-alphanumeric — matches the key format in master_games.json
    return re.sub(r"[^a-z0-9]", "", cleaned)


def _simple_key(name: str) -> str:
    """Simpler key — just strip everything non-alphanumeric, no noise removal."""
    import re
    return re.sub(r"[^a-z0-9]", "", name.lower())


def lookup_exodos(name: str) -> dict | None:
    """Return the ExoDOS entry for a game name.

    Strategy:
    1. Exact key match
    2. Simple key match (no noise stripping)
    3. Containment match — key inside query or query inside key (min 5 chars)
    4. Token match — every word in the query appears in the title
    Returns None if no confident match found.
    """
    db = load_exodos()
    if not db:
        return None

    key  = exodos_key(name)
    key2 = _simple_key(name)
    if not key and not key2:
        return None

    # 1. Exact match on either key form
    if key in db:
        return db[key]
    if key2 in db:
        return db[key2]

    # 2. Containment match — try both key forms
    MIN_OVERLAP = 5
    candidates = []
    for k, v in db.items():
        title_key = _simple_key(v.get("title", ""))
        for q in (key, key2):
            if not q or len(q) < MIN_OVERLAP:
                continue
            if q in k or k in q or q in title_key:
                overlap = min(len(q), len(k))
                score = overlap - abs(len(q) - len(k))
                candidates.append((score, k, v))
                break

    if candidates:
        candidates.sort(key=lambda x: x[0], reverse=True)
        best_score, best_key, best_entry = candidates[0]
        longer = max(len(key2 or key), len(best_key))
        overlap = min(len(key2 or key), len(best_key))
        if longer > 0 and overlap / longer >= 0.70:
            return best_entry

    # 3. Token match — split name into words, check all appear in title
    tokens = [t for t in re.sub(r"[^a-z0-9]", " ", name.lower()).split() if len(t) >= 3]
    if len(tokens) >= 2:
        for k, v in db.items():
            title_low = v.get("title", "").lower()
            if all(t in title_low for t in tokens):
                return v

    return None


def search_exodos(query: str) -> list:
    """Return list of (key, entry) tuples matching a search query."""
    db = load_exodos()
    if not db:
        return []
    q = exodos_key(query)
    q2 = _simple_key(query)
    results = []
    seen = set()
    for k, v in db.items():
        title_key = _simple_key(v.get("title", ""))
        if (q and (q in k or q in title_key)) or (q2 and (q2 in k or q2 in title_key)):
            if k not in seen:
                seen.add(k)
                results.append((k, v))
    return results


# Folder names that indicate a bundled emulator — skip exes inside these
DOSBOX_WRAPPER_NAMES = {"dosbox", "dosbox-staging", "scummvm", "boxer"}

# Known good launcher bat names inside game subfolders
GOOD_BAT_NAMES = {"command.bat", "play.bat", "start.bat", "game.bat", "run.bat", "launch.bat"}

def score_exe(exe: Path, root: Path, stem: str) -> int:
    """Score an EXE/BAT candidate; higher = more likely the main game launcher."""
    name     = exe.name.lower()
    namestem = exe.stem.lower()
    ext      = exe.suffix.lower()
    score    = 0

    # Depth from root (0 = at root, 1 = one subfolder deep, etc.)
    depth = len(exe.relative_to(root).parts) - 1

    # ── Penalise root-level .bat named after the game folder ──────────────────
    # These are almost always Windows OS launchers, not DOS game files
    if ext == ".bat" and depth == 0:
        score -= 8
        # Extra penalty if it matches the stem (e.g. CommandAndConquer.bat)
        if namestem == stem.lower() or namestem in stem.lower().replace("-","").replace("_",""):
            score -= 4

    # ── Known good launcher bat names inside subfolders ───────────────────────
    if ext == ".bat" and depth > 0 and name in GOOD_BAT_NAMES:
        score += 8

    # ── Prefer files one level deep (inside main game subfolder) ──────────────
    if depth == 1:
        score += 5
    elif depth == 0:
        score += 2
    elif depth == 2:
        score += 1

    # ── Exact exe name match to game stem ─────────────────────────────────────
    if namestem == stem.lower() and ext == ".exe":
        score += 10

    # ── Penalise emulator folders ──────────────────────────────────────────────
    parent_name = exe.parent.name.lower()
    if any(d in parent_name for d in DOSBOX_WRAPPER_NAMES):
        score -= 15

    # ── Penalise known setup/install/utility names ─────────────────────────────
    if name in LAUNCHER_NAMES:
        score -= 3
    for bad in SETUP_NAMES:
        if bad in name:
            score -= 5

    # ── Penalise utility folders ───────────────────────────────────────────────
    for util in ("ultrasnd", "ultrasnds", "midi", "sound", "audio", "install"):
        if util in str(exe.parent).lower():
            score -= 6

    return score


def detect_exe(game_dir: Path, stem: str) -> tuple:
    """Return (all_launchers, best_guess) from extracted game directory.
    Considers both .exe and .bat files; best score wins automatically.
    """
    exes = list(game_dir.rglob("*.exe")) + list(game_dir.rglob("*.EXE"))
    bats = list(game_dir.rglob("*.bat")) + list(game_dir.rglob("*.BAT"))
    all_files = list({f.resolve() for f in exes + bats})
    if not all_files:
        return [], None
    if len(all_files) == 1:
        return all_files, all_files[0]
    scored = sorted(all_files, key=lambda e: score_exe(e, game_dir, stem), reverse=True)
    top, second = scored[0], scored[1]
    ambiguous = abs(score_exe(top, game_dir, stem) - score_exe(second, game_dir, stem)) <= 3
    return scored, None if ambiguous else top


def extract_archive(archive: Path, dest: Path) -> None:
    """Extract a zip/7z/rar/tar archive to dest."""
    suffix   = archive.suffix.lower()
    suffixes = [s.lower() for s in archive.suffixes]
    if suffix == ".zip":
        with zipfile.ZipFile(archive) as zf:
            zf.extractall(dest)
    elif suffix == ".7z":
        sevenzip = (str(TOOLS_7ZA) if TOOLS_7ZA.exists()
                    else shutil.which("7z") or shutil.which("7za") or shutil.which("7zr"))
        if not sevenzip:
            raise RuntimeError("7za.exe not found. Place it in the tools\\ folder.")
        result = subprocess.run(
            [sevenzip, "x", str(archive), "-o" + str(dest), "-y"],
            capture_output=True, text=True
        )
        if result.returncode != 0:
            raise RuntimeError("7z extraction failed: " + (result.stderr or result.stdout))
    elif suffix == ".rar":
        # Use bundled 7za.exe — it handles RAR natively, no UnRAR needed
        sevenzip = (str(TOOLS_7ZA) if TOOLS_7ZA.exists()
                    else shutil.which("7z") or shutil.which("7za"))
        if not sevenzip:
            raise RuntimeError("7za.exe not found. Place it in the tools\\ folder.")
        result = subprocess.run(
            [sevenzip, "x", str(archive), "-o" + str(dest), "-y"],
            capture_output=True, text=True
        )
        if result.returncode != 0:
            raise RuntimeError("RAR extraction failed: " + (result.stderr or result.stdout))
    elif suffix in (".gz", ".tgz") or ".tar" in suffixes:
        with tarfile.open(archive) as tf:
            tf.extractall(dest)
    else:
        raise RuntimeError(f"Unsupported archive format: {archive.suffix}")


# ── App ──────────────────────────────────────────────────────────────────────

class App:
    """Main AutoDOS application."""

    def __init__(self, root: tk.Tk):
        self.root    = root
        self.library: list = []
        self.dosbox  = find_dosbox()

        self._setup_window()
        self._build_ui()
        self._load_library()

    # ── Window setup ──────────────────────────────────────────────────────

    def _setup_window(self):
        """Configure the root window."""
        self.root.title("AutoDOS")
        self.root.configure(bg=BG)
        self.root.geometry("520x700")
        self.root.minsize(480, 600)

        if ICON_FILE.exists():
            try:
                self.root.iconbitmap(str(ICON_FILE))
            except Exception:
                pass

        style = ttk.Style(self.root)
        style.theme_use("clam")
        style.configure("TScrollbar", background=BTN_BG, troughcolor=LIST_BG, borderwidth=0)
        style.configure("Pill.TButton",
                        background=BTN_BG, foreground=TEXT,
                        relief="flat", borderwidth=0,
                        padding=(16, 8), font=("TkDefaultFont", 11))
        style.map("Pill.TButton",
                  background=[("active", BTN_ACTIVE)],
                  relief=[("active", "flat")])

    # ── UI Build ──────────────────────────────────────────────────────────

    def _build_ui(self):
        """Construct all UI widgets."""
        self._build_logo()
        self._build_list()
        self._build_buttons()
        tk.Label(self.root, text="Double-click to launch  ·  Right-click to change EXE or remove",
                 bg=BG, fg=TEXT, font=("TkDefaultFont", 9, "bold")
                 ).pack(side=tk.BOTTOM, pady=(0, 6))

    def _build_logo(self):
        """Load and display the logo image."""
        self.logo_img = None
        if LOGO_FILE.exists():
            try:
                from PIL import Image, ImageTk
                img = Image.open(LOGO_FILE).convert("RGBA")
                img.thumbnail((200, 160), Image.LANCZOS)
                self.logo_img = ImageTk.PhotoImage(img)
            except Exception:
                try:
                    self.logo_img = tk.PhotoImage(file=str(LOGO_FILE))
                except Exception:
                    pass

        if self.logo_img:
            lbl = tk.Label(self.root, image=self.logo_img, bg=BG, bd=0)
            lbl.image = self.logo_img  # keep reference — prevents GC on Windows
            lbl.pack(pady=(18, 10))
        else:
            tk.Label(self.root, text="AutoDOS", bg=BG, fg=TEXT,
                     font=("TkDefaultFont", 28, "bold")).pack(pady=(18, 10))

    def _build_list(self):
        """Build the scrollable game library panel."""
        frame = tk.Frame(self.root, bg=BG, padx=12)
        frame.pack(fill=tk.BOTH, expand=True, padx=0, pady=(0, 8))

        container = tk.Frame(frame, bg=BORDER, bd=1, relief="flat")
        container.pack(fill=tk.BOTH, expand=True)

        inner = tk.Frame(container, bg=LIST_BG)
        inner.pack(fill=tk.BOTH, expand=True, padx=1, pady=1)

        self.listbox = tk.Listbox(
            inner,
            bg=LIST_BG, fg=TEXT,
            selectbackground=SEL_BG, selectforeground=TEXT,
            activestyle="none", relief="flat", bd=0,
            font=("TkDefaultFont", 13),
            highlightthickness=0,
            selectmode=tk.SINGLE,
        )
        self.listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.listbox.bind("<Double-Button-1>", lambda e: self._launch_selected())
        self.listbox.bind("<<ListboxSelect>>", self._on_select)
        self.listbox.bind("<ButtonRelease-3>", self._show_context_menu)

        sb = ttk.Scrollbar(inner, orient=tk.VERTICAL, command=self.listbox.yview)
        sb.pack(side=tk.RIGHT, fill=tk.Y)
        self.listbox.configure(yscrollcommand=sb.set)

    def _build_buttons(self):
        """Build the bottom button bar."""
        bar = tk.Frame(self.root, bg=BG)
        bar.pack(fill=tk.X, padx=14, pady=(0, 4))

        self.btn_launch = ttk.Button(bar, text="▶  Launch",
                                     style="Pill.TButton",
                                     command=self._launch_selected)
        self.btn_launch.pack(side=tk.LEFT, padx=(0, 6))
        self.btn_launch.state(["disabled"])

        ttk.Button(bar, text="＋  Add Zip",
                   style="Pill.TButton",
                   command=self._add_archive).pack(side=tk.LEFT, padx=(0, 6))

        ttk.Button(bar, text="💿  Add CD",
                   style="Pill.TButton",
                   command=self._add_cd).pack(side=tk.LEFT)

        ttk.Button(bar, text="🗑  Remove",
                   style="Pill.TButton",
                   command=self._remove_selected).pack(side=tk.RIGHT)

    # ── Library ───────────────────────────────────────────────────────────

    def _load_library(self):
        """Load library.json and populate the listbox."""
        if LIBRARY_FILE.exists():
            try:
                self.library = json.loads(LIBRARY_FILE.read_text())
            except Exception:
                self.library = []
        self._refresh_list()

    def _save_library(self):
        """Persist library to library.json."""
        LIBRARY_FILE.write_text(json.dumps(self.library, indent=2))

    def _refresh_list(self):
        """Repopulate the listbox from self.library."""
        self.listbox.delete(0, tk.END)
        for i, entry in enumerate(self.library):
            self.listbox.insert(tk.END, f"  {entry['name']}")
            bg = LIST_BG if i % 2 == 0 else ALT_ROW_BG
            self.listbox.itemconfig(i, bg=bg)
        self.btn_launch.state(["disabled"])

    def _on_select(self, _event=None):
        """Enable/disable Launch button based on selection."""
        if self.listbox.curselection():
            self.btn_launch.state(["!disabled"])
        else:
            self.btn_launch.state(["disabled"])

    # ── Context Menu ──────────────────────────────────────────────────────

    def _show_context_menu(self, event):
        """Show right-click context menu only when clicking on an actual game row."""
        idx = self.listbox.nearest(event.y)

        # Bail out if no games, or click is in empty space below last row
        if not self.library or idx < 0 or idx >= len(self.library):
            return

        # Check the click is actually within the row's bounding box
        bbox = self.listbox.bbox(idx)
        if not bbox:
            return
        _, row_y, _, row_h = bbox
        if event.y < row_y or event.y > row_y + row_h:
            return

        self.listbox.selection_clear(0, tk.END)
        self.listbox.selection_set(idx)
        self._on_select()

        menu = tk.Menu(self.root, tearoff=0, bg=BTN_BG, fg=TEXT,
                       activebackground=SEL_BG, activeforeground=TEXT,
                       relief="flat", bd=0, font=("TkDefaultFont", 11))
        menu.add_command(label="⚙  Game Settings", command=lambda: self._show_game_settings(self.library[idx]))
        menu.add_command(label="🔄  Change EXE", command=lambda: self._show_exe_picker(self.library[idx]))
        menu.add_separator()
        menu.add_command(label="🗑  Remove", command=self._remove_selected)

        # Dismiss on any click outside
        menu.bind("<FocusOut>", lambda e: menu.unpost())
        self.root.bind("<Button-1>", lambda e: menu.unpost(), add="+")

        # Force window to be fully rendered before computing popup position
        self.root.update_idletasks()
        x = self.root.winfo_pointerx()
        y = self.root.winfo_pointery()

        try:
            menu.tk_popup(x, y)
        finally:
            menu.grab_release()

    # ── Ingest Pipeline ───────────────────────────────────────────────────

    def _add_archive(self):
        """Open file picker using tkinter dialog (Windows native)."""
        path = filedialog.askopenfilename(
            title="Select a game archive",
            filetypes=ARCHIVE_FILTERS,
            parent=self.root,
        )
        if not path:
            return
        archive = Path(path)

        if any(e["archive_name"] == archive.name for e in self.library):
            if not messagebox.askyesno("Duplicate",
                    f"'{archive.name}' is already in your library. Re-import it?",
                    parent=self.root):
                return

        stem = archive.stem.split(".")[0]
        dest = GAMES_DIR / stem
        GAMES_DIR.mkdir(exist_ok=True)

        threading.Thread(
            target=self._ingest_thread,
            args=(archive, dest, stem),
            daemon=True,
        ).start()

    def _ingest_thread(self, archive: Path, dest: Path, stem: str):
        """Worker: extract, detect EXE, update library."""
        try:
            dest.mkdir(exist_ok=True)
            extract_archive(archive, dest)
        except Exception as e:
            self.root.after(0, lambda: messagebox.showerror("Extraction Failed", str(e), parent=self.root))
            return

        exes, best = detect_exe(dest, stem)

        if not exes:
            shutil.rmtree(dest, ignore_errors=True)
            self.root.after(0, lambda: messagebox.showerror(
                "No Executable Found",
                "No .exe files were found in this archive.",
                parent=self.root))
            return

        display_name = stem.replace("-", " ").replace("_", " ").title()
        exo = lookup_exodos(display_name)

        # ExoDOS match found — apply silently, no popup

        entry = {
            "id":             stem,
            "name":           exo["title"] if exo and "title" in exo else display_name,
            "archive_name":   archive.name,
            "extracted_path": str(dest),
            "exe_path":       "",
            "date_added":     str(date.today()),
            "cycles":         str(exo["cycles"]) if exo and "cycles" in exo else "3000",
            "memsize":        snap_memsize(int(exo["memsize"])) if exo and "memsize" in exo else 16,
            "xms":            bool(exo.get("xms", True)) if exo else True,
            "ems":            bool(exo.get("ems", True)) if exo else True,
        }

        if best:
            entry["exe_path"] = str(best.relative_to(dest))
            self.library.append(entry)
            self._save_library()
            self.root.after(0, self._refresh_list)
            self.root.after(0, lambda: self._launch_entry(entry))
        else:
            self.root.after(0, lambda: ExePickerModal(
                self.root, exes, dest, entry,
                on_confirm=self._on_exe_picked,
            ))

    def _on_exe_picked(self, entry: dict, chosen: Path, dest: Path):
        """Called when user picks an EXE from the picker modal."""
        entry["exe_path"] = str(chosen.relative_to(dest))
        self.library = [e for e in self.library if e["id"] != entry["id"]]
        self.library.append(entry)
        self._save_library()
        self._refresh_list()
        self._launch_entry(entry)

    # ── CD Add Pipeline ───────────────────────────────────────────────────────

    def _add_cd(self):
        """Pick a pre-extracted game folder — scan for ISOs and exe on disc."""
        folder = filedialog.askdirectory(
            title="Select game folder",
            parent=self.root,
        )
        if not folder:
            return
        dest = Path(folder)
        stem = dest.name
        if any(e["extracted_path"] == str(dest) for e in self.library):
            if not messagebox.askyesno("Duplicate",
                    "'" + stem + "' is already in your library. Re-import it?",
                    parent=self.root):
                return
        threading.Thread(
            target=self._ingest_cd_thread,
            args=(dest, stem),
            daemon=True,
        ).start()

    def _ingest_cd_thread(self, dest: Path, stem: str):
        """Worker: find ISOs, scan first ISO for exe candidates, show picker."""
        display_name = stem.replace("-", " ").replace("_", " ").title()
        exo          = lookup_exodos(display_name)
        cd_isos      = detect_cd_source(dest)

        if not cd_isos:
            self.root.after(0, lambda: messagebox.showerror(
                "No Disc Images Found",
                "No ISO, BIN, CUE, or IMG files found in that folder.",
                parent=self.root))
            return

        # Build base entry with ExoDOS settings if matched
        entry = {
            "id":             stem,
            "name":           exo["title"] if exo and "title" in exo else display_name,
            "archive_name":   stem,
            "extracted_path": str(dest),
            "exe_path":       "",
            "date_added":     str(date.today()),
            "cycles":         str(exo["cycles"]) if exo and "cycles" in exo else "3000",
            "memsize":        snap_memsize(int(exo["memsize"])) if exo and "memsize" in exo else 16,
            "xms":            bool(exo.get("xms", True)) if exo else True,
            "ems":            bool(exo.get("ems", True)) if exo else True,
            "cd_isos":        cd_isos,
            "cd_mount":       True,
            "cd_exe":         str(exo.get("exe", "")) if exo else "",
        }

        # If ExoDOS gave us the exe, use it directly
        if entry["cd_exe"]:
            self.library.append(entry)
            self._save_library()
            self.root.after(0, self._refresh_list)
            self.root.after(0, lambda: self._show_disc_tip(entry))
            self.root.after(0, lambda: self._launch_entry(entry))
            return

        # No ExoDOS exe — scan first ISO with 7za to find candidates
        exe_candidates = scan_iso_for_exes(cd_isos[0])

        if not exe_candidates:
            # Nothing found in ISO — add to library, user can set via Game Settings
            self.library.append(entry)
            self._save_library()
            self.root.after(0, self._refresh_list)
            self.root.after(0, lambda: messagebox.showwarning(
                "No Exe Found in Disc",
                "Could not detect a game executable inside the disc image.\n"
                "Right-click the game → Game Settings to set the exe manually.",
                parent=self.root))
            return

        # Show ISO exe picker so user selects which exe to run
        self.library.append(entry)
        self._save_library()
        self.root.after(0, self._refresh_list)
        self.root.after(0, lambda: IsoExePickerModal(
            self.root, exe_candidates, entry,
            on_confirm=self._on_iso_exe_picked,
        ))

    def _on_iso_exe_picked(self, entry: dict, cd_exe: str):
        """Called when user picks an exe from the ISO picker."""
        entry["cd_exe"] = cd_exe
        for i, e in enumerate(self.library):
            if e["id"] == entry["id"]:
                self.library[i] = entry
                break
        self._save_library()
        self._show_disc_tip(entry)
        self._launch_entry(entry)

    def _show_disc_tip(self, entry: dict):
        """Show multi-disc tip if game has more than one ISO."""
        cd_isos = entry.get("cd_isos", [])
        if len(cd_isos) > 1:
            names = "\n".join("  Disc " + str(i+1) + ": " + Path(cd_isos[i]).name
                               for i in range(len(cd_isos)))
            msg = (entry["name"] + " has " + str(len(cd_isos)) + " discs:\n" +
                   names + "\n\nDisc 1 will be mounted as D: on launch.\n"
                   "Press Ctrl+F4 in DOSBox to swap discs.")
            messagebox.showinfo("Multi-Disc Game", msg, parent=self.root)

    # ── Launch ────────────────────────────────────────────────────────────

    def _launch_selected(self):
        """Launch the currently selected game — always read fresh from library."""
        sel = self.listbox.curselection()
        if not sel:
            return
        # Re-read from library to pick up any settings changes
        entry = self.library[sel[0]]
        self._launch_entry(entry)

    def _launch_entry(self, entry: dict):
        """Launch a game entry via DOSBox.

        Case 1 — SIMPLE: exe on C:, optional ISO on D:
        Case 2 — CD_ONLY: imgmount all ISOs as D:, boot from D:, run cd_exe
        """
        if not self.dosbox:
            messagebox.showerror(
                "DOSBox Not Found",
                "DOSBox Staging not found.\n"
                "Place dosbox.exe in the dosbox\\ folder next to autodos_win.py,\n"
                "or download from: https://dosbox-staging.github.io",
                parent=self.root)
            return

        extracted = Path(entry["extracted_path"])
        exe_rel   = entry.get("exe_path", "")
        cd_isos   = entry.get("cd_isos", [])
        cd_mount  = entry.get("cd_mount", False)
        cd_exe    = entry.get("cd_exe", "")
        binary, prefix = self.dosbox

        # ── Cycles ───────────────────────────────────────────────────────────
        import re as _re
        cycles_str  = str(entry.get("cycles", "3000"))
        memsize     = snap_memsize(int(entry.get("memsize", 16)))
        limit_match = _re.match(r"max\s+(?:limit\s+)?(\d+)", cycles_str, _re.IGNORECASE)
        if limit_match:
            conf_cycles = limit_match.group(1)
        elif cycles_str.lower() in ("max", "auto"):
            conf_cycles = "max"
        else:
            conf_cycles = cycles_str

        def make_imgmount(isos):
            quoted = " ".join(f'"{iso}"' if " " in iso else iso for iso in isos)
            return f"imgmount D {quoted} -t iso"

        # ── Case 2: CD-only — exe lives on the disc ───────────────────────────
        if cd_mount and cd_isos:
            if not cd_exe:
                messagebox.showwarning(
                    "No Disc Exe Set",
                    "No executable set for this CD game.\n"
                    "Remove and re-add via Add CD to scan the disc.",
                    parent=self.root)
                return
            c_path  = str(extracted)
            mount_c = f'mount c "{c_path}"' if " " in c_path else f"mount c {c_path}"
            run_cmd = f'"{cd_exe}"' if " " in cd_exe else cd_exe
            cmd = [binary] + prefix + [
                "-conf", str(ASSET_DIR / "dosbox.conf"),
                "-c", f"cpu_cycles {conf_cycles}",
                "-c", f"cpu_cycles_protected {conf_cycles}",
                "-c", f"set memsize={memsize}",
                "-c", mount_c,
                "-c", make_imgmount(cd_isos),
                "-c", "D:",
                "-c", run_cmd,
                "-c", "exit",
            ]
            threading.Thread(target=self._dosbox_thread, args=(cmd, entry), daemon=True).start()
            return

        # ── Case 1: exe on C:, optional ISO on D: ────────────────────────────
        if not exe_rel:
            self._show_exe_picker(entry)
            return

        exe_name    = Path(exe_rel).name
        exe_dir     = (extracted / exe_rel).parent
        exe_dir_str = str(exe_dir)
        mount_c     = f'mount c "{exe_dir_str}"' if " " in exe_dir_str else f"mount c {exe_dir_str}"
        run_cmd     = f'"{exe_name}"' if " " in exe_name else exe_name

        cmd = [binary] + prefix + [
            "-conf", str(ASSET_DIR / "dosbox.conf"),
            "-c", f"cpu_cycles {conf_cycles}",
            "-c", f"cpu_cycles_protected {conf_cycles}",
            "-c", f"set memsize={memsize}",
            "-c", mount_c,
        ]
        if cd_isos:
            cmd += ["-c", make_imgmount(cd_isos)]
        cmd += ["-c", "c:", "-c", run_cmd, "-c", "exit"]
        threading.Thread(target=self._dosbox_thread, args=(cmd, entry), daemon=True).start()

    def _dosbox_thread(self, cmd: list, entry: dict):
        """Worker: run DOSBox and handle non-zero exit."""
        proc = subprocess.Popen(cmd, shell=False)
        proc.wait()
        if proc.returncode != 0:
            self.root.after(0, lambda: self._show_exe_picker(entry))

    def _show_game_settings(self, entry: dict):
        """Open per-game DOSBox settings dialog."""
        GameSettingsModal(self.root, entry, on_save=self._on_settings_saved)

    def _on_settings_saved(self, entry: dict):
        """Save updated game settings to library."""
        for i, e in enumerate(self.library):
            if e["id"] == entry["id"]:
                self.library[i] = entry
                break
        self._save_library()

    def _show_exe_picker(self, entry: dict):
        """Open EXE picker modal for failed or ambiguous launch."""
        dest = Path(entry["extracted_path"])
        exes, _ = detect_exe(dest, entry["id"])
        if not exes:
            messagebox.showerror("Error", "No executables found in game directory.", parent=self.root)
            return
        ExePickerModal(self.root, exes, dest, entry, on_confirm=self._on_exe_picked)

    # ── Remove ────────────────────────────────────────────────────────────

    def _remove_selected(self):
        """Remove selected game from library.
        Only offers to delete files if the folder is inside AutoDOS games dir.
        External CD game folders are never deleted.
        """
        sel = self.listbox.curselection()
        if not sel:
            return
        entry      = self.library[sel[0]]
        ext_path   = Path(entry["extracted_path"])
        is_managed = ext_path.is_relative_to(GAMES_DIR)

        if is_managed:
            result = messagebox.askyesnocancel(
                "Remove Game",
                "Remove '" + entry["name"] + "' from your library?\n\n"
                "Yes = remove entry AND delete files\n"
                "No  = remove entry only, keep files",
                parent=self.root)
            if result is None:
                return
            if result:
                shutil.rmtree(entry["extracted_path"], ignore_errors=True)
        else:
            result = messagebox.askyesno(
                "Remove Game",
                "Remove '" + entry["name"] + "' from your library?\n"
                "The game folder will not be deleted.",
                parent=self.root)
            if not result:
                return

        self.library.pop(sel[0])
        self._save_library()
        self._refresh_list()


# ── Modals ───────────────────────────────────────────────────────────────────

class ExePickerModal:
    """Modal dialog for selecting an EXE when auto-detection is ambiguous or fails."""

    def __init__(self, parent: tk.Tk, exes: list, dest: Path,
                 entry: dict, on_confirm):
        self.dest       = dest
        self.entry      = entry
        self.on_confirm = on_confirm
        self.exes       = exes

        self.win = tk.Toplevel(parent)
        self.win.title("Choose Executable")
        self.win.configure(bg=BG)
        self.win.geometry("460x320")
        self.win.resizable(False, False)
        self.win.transient(parent)
        self.win.lift()
        self.win.focus_force()

        tk.Label(self.win,
                 text="Multiple executables found.\nSelect the correct one to launch:",
                 bg=BG, fg=TEXT, font=("TkDefaultFont", 11),
                 justify=tk.LEFT).pack(anchor="w", padx=16, pady=(16, 8))

        frame = tk.Frame(self.win, bg=BORDER, bd=1)
        frame.pack(fill=tk.BOTH, expand=True, padx=16, pady=(0, 12))

        self.lb = tk.Listbox(
            frame, bg=LIST_BG, fg=TEXT,
            selectbackground=SEL_BG, selectforeground=TEXT,
            activestyle="none", relief="flat", bd=0,
            font=("TkDefaultFont", 11), highlightthickness=0,
            exportselection=False)
        self.lb.pack(fill=tk.BOTH, expand=True, padx=1, pady=1)
        self.lb.bind("<Double-Button-1>", lambda e: self._confirm())
        self.lb.bind("<Return>", lambda e: self._confirm())

        for exe in exes:
            try:
                rel = exe.relative_to(dest)
            except ValueError:
                rel = exe
            self.lb.insert(tk.END, f"  {rel}")

        self.lb.selection_set(0)
        self.lb.focus_set()

        btn_frame = tk.Frame(self.win, bg=BG)
        btn_frame.pack(fill=tk.X, padx=16, pady=(0, 14))

        style = ttk.Style()
        style.configure("Pill.TButton", background=BTN_BG, foreground=TEXT,
                        relief="flat", borderwidth=0, padding=(16, 8),
                        font=("TkDefaultFont", 11))
        style.map("Pill.TButton", background=[("active", BTN_ACTIVE)])

        ttk.Button(btn_frame, text="▶  Launch", style="Pill.TButton",
                   command=self._confirm).pack(side=tk.LEFT, padx=(0, 8))
        ttk.Button(btn_frame, text="Cancel", style="Pill.TButton",
                   command=self.win.destroy).pack(side=tk.LEFT)

    def _confirm(self):
        """Confirm selection and invoke callback."""
        sel = self.lb.curselection()
        if not sel:
            return
        chosen = self.exes[sel[0]]
        self.win.destroy()
        self.on_confirm(self.entry, chosen, self.dest)


# ── Game Settings Modal ──────────────────────────────────────────────────────

class GameSettingsModal:
    """Per-game DOSBox settings dialog."""

    def __init__(self, parent: tk.Tk, entry: dict, on_save):
        self.entry   = dict(entry)
        self.on_save = on_save
        self.parent  = parent

        self.win = tk.Toplevel(parent)
        self.win.title("Game Settings — " + entry["name"])
        self.win.configure(bg=BG)
        self.win.geometry("480x520")
        self.win.minsize(480, 520)
        self.win.resizable(False, False)
        self.win.transient(parent)
        self.win.lift()
        self.win.focus_force()

        self._build()

    def _build(self):
        entry = self.entry

        # ── Header ──────────────────────────────────────────────────────
        exo = lookup_exodos(entry["name"])
        if exo:
            status = "ExoDOS match: " + exo.get("title", entry["name"])
            color  = "#4a9960"
        else:
            status = "No ExoDOS match — set manually or search below"
            color  = MUTED

        tk.Label(self.win, text=status, bg=BG, fg=color,
                 font=("TkDefaultFont", 9, "bold")
                 ).pack(anchor="w", padx=16, pady=(14, 0))

        tk.Frame(self.win, bg=BORDER, height=1).pack(fill=tk.X, padx=16, pady=10)

        # ── Settings form ────────────────────────────────────────────────
        form = tk.Frame(self.win, bg=BG)
        form.pack(fill=tk.X, padx=16)
        form.columnconfigure(1, weight=1)

        def field(label, var, row, hint=None):
            tk.Label(form, text=label, bg=BG, fg=TEXT,
                     font=("TkDefaultFont", 11), anchor="w", width=14
                     ).grid(row=row, column=0, sticky="w", pady=5)
            e = tk.Entry(form, textvariable=var, bg=LIST_BG, fg=TEXT,
                         relief="flat", bd=0, font=("TkDefaultFont", 11),
                         highlightthickness=1, highlightbackground=BORDER)
            e.grid(row=row, column=1, sticky="ew", pady=5)
            if hint:
                tk.Label(form, text=hint, bg=BG, fg=MUTED,
                         font=("TkDefaultFont", 8)
                         ).grid(row=row+1, column=1, sticky="w")

        def checkbox(label, var, row):
            tk.Label(form, text=label, bg=BG, fg=TEXT,
                     font=("TkDefaultFont", 11), anchor="w", width=14
                     ).grid(row=row, column=0, sticky="w", pady=5)
            tk.Checkbutton(form, variable=var, bg=BG,
                           activebackground=BG, relief="flat"
                           ).grid(row=row, column=1, sticky="w", pady=5)

        self.cycles_var = tk.StringVar(value=str(entry.get("cycles", "3000")))
        self.mem_var    = tk.StringVar(value=str(entry.get("memsize", 16)))
        self.xms_var    = tk.BooleanVar(value=bool(entry.get("xms", True)))
        self.ems_var    = tk.BooleanVar(value=bool(entry.get("ems", True)))

        field("CPU Cycles:", self.cycles_var, 0,
              "e.g.  3000  |  max  |  max limit 35000")
        field("Mem (MB):", self.mem_var, 2)
        checkbox("XMS:", self.xms_var, 4)
        checkbox("EMS:", self.ems_var, 5)

        tk.Frame(self.win, bg=BORDER, height=1).pack(fill=tk.X, padx=16, pady=10)

        # ── Save button ───────────────────────────────────────────────────
        save_row = tk.Frame(self.win, bg=BG)
        save_row.pack(fill=tk.X, padx=16, pady=(0, 6))

        style = ttk.Style()
        style.configure("Pill.TButton", background=BTN_BG, foreground=TEXT,
                        relief="flat", borderwidth=0, padding=(16, 8),
                        font=("TkDefaultFont", 11))
        style.map("Pill.TButton", background=[("active", BTN_ACTIVE)])

        ttk.Button(save_row, text="💾  Save", style="Pill.TButton",
                   command=self._save).pack(side=tk.LEFT, padx=(0, 8))
        ttk.Button(save_row, text="Cancel", style="Pill.TButton",
                   command=self.win.destroy).pack(side=tk.LEFT)

        tk.Frame(self.win, bg=BORDER, height=1).pack(fill=tk.X, padx=16, pady=(6, 10))

        # ── ExoDOS search ─────────────────────────────────────────────────
        tk.Label(self.win, text="Search ExoDOS Database",
                 bg=BG, fg=TEXT, font=("TkDefaultFont", 11, "bold")
                 ).pack(anchor="w", padx=16, pady=(0, 6))

        search_row = tk.Frame(self.win, bg=BG)
        search_row.pack(fill=tk.X, padx=16, pady=(0, 6))

        self.search_var = tk.StringVar()
        self.search_entry = tk.Entry(search_row, textvariable=self.search_var,
                                     bg=LIST_BG, fg=TEXT, relief="flat", bd=0,
                                     font=("TkDefaultFont", 11),
                                     highlightthickness=1,
                                     highlightbackground=BORDER)
        self.search_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 8))
        self.search_entry.bind("<Return>", lambda e: self._do_search())
        self.search_entry.bind("<KeyRelease>", self._on_key)

        ttk.Button(search_row, text="Search", style="Pill.TButton",
                   command=self._do_search).pack(side=tk.LEFT)

        # Results listbox
        res_frame = tk.Frame(self.win, bg=BORDER, bd=1)
        res_frame.pack(fill=tk.BOTH, expand=True, padx=16, pady=(0, 6))

        self.results_lb = tk.Listbox(
            res_frame, bg=LIST_BG, fg=TEXT,
            selectbackground=SEL_BG, selectforeground=TEXT,
            activestyle="none", relief="flat", bd=0,
            font=("TkDefaultFont", 11), highlightthickness=0,
            exportselection=False, height=5)
        self.results_lb.pack(side=tk.LEFT, fill=tk.BOTH, expand=True,
                             padx=1, pady=1)
        self.results_lb.bind("<Double-Button-1>", lambda e: self._apply_result())
        self.results_lb.bind("<Return>", lambda e: self._apply_result())

        sb = ttk.Scrollbar(res_frame, orient=tk.VERTICAL,
                           command=self.results_lb.yview)
        sb.pack(side=tk.RIGHT, fill=tk.Y)
        self.results_lb.configure(yscrollcommand=sb.set)

        self.search_matches = []

        apply_row = tk.Frame(self.win, bg=BG)
        apply_row.pack(fill=tk.X, padx=16, pady=(0, 12))

        ttk.Button(apply_row, text="✓  Apply & Save",
                   style="Pill.TButton",
                   command=self._apply_result).pack(side=tk.LEFT)

        self.status_label = tk.Label(self.win, text="", bg=BG, fg=MUTED,
                                     font=("TkDefaultFont", 9))
        self.status_label.pack(anchor="w", padx=16, pady=(0, 8))

    def _on_key(self, event):
        """Live search as user types."""
        if len(self.search_var.get()) >= 3:
            self._do_search()

    def _do_search(self):
        """Search ExoDOS and populate results list."""
        q = self.search_var.get().strip()
        if not q:
            return
        results = search_exodos(q)
        self.results_lb.delete(0, tk.END)
        self.search_matches = results[:20]
        if not results:
            self.status_label.config(text="No matches found.", fg=MUTED)
            return
        for k, v in self.search_matches:
            cycles = v.get("cycles", "?")
            mem    = v.get("memsize", "?")
            self.results_lb.insert(
                tk.END,
                f"  {v.get('title', k)}   [{cycles} cycles / {mem}MB]"
            )
        self.results_lb.selection_set(0)
        self.status_label.config(
            text=f"{len(results)} result(s) — double-click or Apply to use",
            fg=MUTED)

    def _apply_result(self):
        """Apply the selected ExoDOS result and save immediately."""
        sel = self.results_lb.curselection()
        if not sel:
            return
        _, exo = self.search_matches[sel[0]]
        self.cycles_var.set(str(exo.get("cycles", "auto")))
        self.mem_var.set(str(exo.get("memsize", 16)))
        self.xms_var.set(bool(exo.get("xms", True)))
        self.ems_var.set(bool(exo.get("ems", True)))
        # Auto-save so user doesn't need to click Save separately
        self._save()

    def _save(self):
        """Save settings to entry and call callback."""
        try:
            memsize = int(self.mem_var.get())
        except ValueError:
            memsize = 16
        self.entry["cycles"]  = self.cycles_var.get().strip()
        self.entry["memsize"] = memsize
        self.entry["xms"]     = self.xms_var.get()
        self.entry["ems"]     = self.ems_var.get()
        self.win.destroy()
        self.on_save(self.entry)


# ── ISO Exe Picker Modal ─────────────────────────────────────────────────────

class IsoExePickerModal:
    """Pick which exe inside the ISO to launch the game with."""

    def __init__(self, parent, exe_candidates: list, entry: dict, on_confirm):
        self.exe_candidates = exe_candidates
        self.entry          = entry
        self.on_confirm     = on_confirm

        self.win = tk.Toplevel(parent)
        self.win.title("Select Game Executable")
        self.win.configure(bg=BG)
        self.win.geometry("420x300")
        self.win.resizable(False, False)
        self.win.transient(parent)
        self.win.lift()
        self.win.focus_force()

        tk.Label(self.win,
                 text="Executables found on disc — select the one that runs the game:",
                 bg=BG, fg=TEXT, font=("TkDefaultFont", 11),
                 wraplength=380, justify=tk.LEFT
                 ).pack(anchor="w", padx=16, pady=(16, 8))

        frame = tk.Frame(self.win, bg=BORDER, bd=1)
        frame.pack(fill=tk.BOTH, expand=True, padx=16, pady=(0, 12))

        self.lb = tk.Listbox(
            frame, bg=LIST_BG, fg=TEXT,
            selectbackground=SEL_BG, selectforeground=TEXT,
            activestyle="none", relief="flat", bd=0,
            font=("TkDefaultFont", 12), highlightthickness=0,
            exportselection=False)
        self.lb.pack(fill=tk.BOTH, expand=True, padx=1, pady=1)
        self.lb.bind("<Double-Button-1>", lambda e: self._confirm())
        self.lb.bind("<Return>",          lambda e: self._confirm())

        for name in exe_candidates:
            self.lb.insert(tk.END, f"  {name}")
        self.lb.selection_set(0)
        self.lb.focus_set()

        btn_frame = tk.Frame(self.win, bg=BG)
        btn_frame.pack(fill=tk.X, padx=16, pady=(0, 14))

        style = ttk.Style()
        style.configure("Pill.TButton", background=BTN_BG, foreground=TEXT,
                        relief="flat", borderwidth=0, padding=(16, 8),
                        font=("TkDefaultFont", 11))
        style.map("Pill.TButton", background=[("active", BTN_ACTIVE)])

        ttk.Button(btn_frame, text="▶  Launch", style="Pill.TButton",
                   command=self._confirm).pack(side=tk.LEFT, padx=(0, 8))
        ttk.Button(btn_frame, text="Cancel", style="Pill.TButton",
                   command=self.win.destroy).pack(side=tk.LEFT)

    def _confirm(self):
        sel = self.lb.curselection()
        if not sel:
            return
        chosen = self.exe_candidates[sel[0]]
        self.win.destroy()
        self.on_confirm(self.entry, chosen)


# ── Entry Point ───────────────────────────────────────────────────────────────

def main():
    """Launch the AutoDOS application."""
    root = tk.Tk()
    App(root)
    root.mainloop()


if __name__ == "__main__":
    main()
