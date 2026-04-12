// autodos.cpp — AutoDOS32 core (Windows XP compatible)
// No std::filesystem, no std::thread, no C++17

#include "autodos.h"
#include "miniz.c"
#include "nlohmann/json.hpp"

#include <algorithm>
#include <cctype>
#include <fstream>
#include <sstream>
#include <windows.h>

using json = nlohmann::json;

namespace AutoDOS {

// ── Win32 filesystem helpers ──────────────────────────────────────────────────

bool pathExists(const std::string& path) {
    DWORD attr = GetFileAttributesA(path.c_str());
    return attr != INVALID_FILE_ATTRIBUTES;
}

bool createDirs(const std::string& path) {
    // Walk path and create each directory level
    std::string cur;
    for (size_t i = 0; i < path.size(); i++) {
        char c = path[i];
        cur += c;
        if ((c == '\\' || c == '/') && cur.size() > 3) {
            CreateDirectoryA(cur.c_str(), nullptr);
        }
    }
    return CreateDirectoryA(path.c_str(), nullptr) || GetLastError() == ERROR_ALREADY_EXISTS;
}

std::string pathJoin(const std::string& a, const std::string& b) {
    if (a.empty()) return b;
    char last = a[a.size()-1];
    if (last == '\\' || last == '/') return a + b;
    return a + "\\" + b;
}

std::string pathFilename(const std::string& path) {
    size_t pos = path.find_last_of("/\\");
    return (pos == std::string::npos) ? path : path.substr(pos + 1);
}

std::string pathStem(const std::string& path) {
    std::string f = pathFilename(path);
    size_t dot = f.rfind('.');
    return (dot == std::string::npos) ? f : f.substr(0, dot);
}

static std::string pathDir(const std::string& path) {
    size_t pos = path.find_last_of("/\\");
    return (pos == std::string::npos) ? "" : path.substr(0, pos);
}

static bool copyFileWin32(const std::string& src, const std::string& dst) {
    return CopyFileA(src.c_str(), dst.c_str(), FALSE) != 0;
}

static void deleteFileWin32(const std::string& path) {
    DeleteFileA(path.c_str());
}

// ── String helpers ────────────────────────────────────────────────────────────

static std::string toLower(std::string s) {
    std::transform(s.begin(), s.end(), s.begin(), ::tolower);
    return s;
}

static std::string toUpper(std::string s) {
    std::transform(s.begin(), s.end(), s.begin(), ::toupper);
    return s;
}

static std::string basename(const std::string& path) {
    return pathFilename(path);
}

static std::string stemOf(const std::string& filename) {
    return pathStem(filename);
}

static std::string extOf(const std::string& filename) {
    std::string b = basename(filename);
    size_t dot = b.rfind('.');
    return (dot == std::string::npos) ? "" : toUpper(b.substr(dot + 1));
}

static std::string dirOf(const std::string& path) {
    std::string normalized = path;
    std::replace(normalized.begin(), normalized.end(), '/', '\\');
    size_t pos = normalized.rfind('\\');
    if (pos == std::string::npos) return "";
    return normalized.substr(0, pos);
}

// ── Blacklist ─────────────────────────────────────────────────────────────────

static const char* EXE_BLACKLIST[] = {
    "setup", "install", "uninst", "uninstall", "patch", "update",
    "config", "cfg", "register", "readme", "read", "help",
    "directx", "dxsetup", "vcredist", "dotnet",
    "dos4gw", "cwsdpmi", "himemx", "emm386",
    "fixsave", "fix", "convert", "copy", "move", nullptr
};

static bool isBlacklisted(const std::string& stem) {
    std::string lower = toLower(stem);
    for (int i = 0; EXE_BLACKLIST[i]; i++) {
        if (lower == EXE_BLACKLIST[i]) return true;
    }
    return false;
}

// ── ZIP entry ─────────────────────────────────────────────────────────────────

struct ZipEntry {
    std::string name;
    int         depth    = 0;
    std::string ext;
    std::string base;
    size_t      compSize = 0;
};

// ── ZIP reader ────────────────────────────────────────────────────────────────

static std::vector<ZipEntry> readZipEntries(const std::string& zipPath) {
    std::vector<ZipEntry> entries;
    mz_zip_archive zip = {};
    if (!mz_zip_reader_init_file(&zip, zipPath.c_str(), 0)) return entries;

    int count = (int)mz_zip_reader_get_num_files(&zip);
    for (int i = 0; i < count; i++) {
        mz_zip_archive_file_stat stat = {};
        if (!mz_zip_reader_file_stat(&zip, i, &stat)) continue;
        if (mz_zip_reader_is_file_a_directory(&zip, i)) continue;

        std::string rawName = stat.m_filename;
        std::replace(rawName.begin(), rawName.end(), '\\', '/');

        std::vector<std::string> parts;
        std::stringstream ss(rawName);
        std::string part;
        while (std::getline(ss, part, '/')) {
            if (!part.empty()) parts.push_back(part);
        }
        if (parts.empty()) continue;

        ZipEntry e;
        e.name     = rawName;
        e.depth    = (int)parts.size() - 1;
        e.base     = toUpper(parts.back());
        e.ext      = extOf(e.base);
        e.compSize = (size_t)stat.m_comp_size;
        entries.push_back(e);
    }
    mz_zip_reader_end(&zip);
    return entries;
}

// ── Fingerprint ───────────────────────────────────────────────────────────────

std::string fingerprint(const std::string& filename) {
    std::string name = basename(filename);
    size_t dot = name.rfind('.');
    if (dot != std::string::npos) name = name.substr(0, dot);
    name = toLower(name);

    if (name.size() >= 7 && (name.substr(0,7) == "dosbox_" || name.substr(0,7) == "dosbox-"))
        name = name.substr(7);

    // Strip (region) [flags]
    std::string result;
    bool inBracket = false;
    for (size_t i = 0; i < name.size(); i++) {
        char c = name[i];
        if (c == '(' || c == '[') { inBracket = true; continue; }
        if (c == ')' || c == ']') { inBracket = false; continue; }
        if (inBracket) continue;
        if (c == ' ' || c == '-' || c == '_' || c == ':' || c == ',' ||
            c == '\'' || c == '.' || c == '!' || c == '?') continue;
        result += c;
    }
    name = result;

    // Strip leading article if first word of original was article
    std::string orig = toLower(basename(filename));
    dot = orig.rfind('.');
    if (dot != std::string::npos) orig = orig.substr(0, dot);
    size_t wordEnd = orig.find_first_of(" -_");
    std::string firstWord = (wordEnd != std::string::npos) ? orig.substr(0, wordEnd) : orig;
    if ((firstWord == "the" || firstWord == "a" || firstWord == "an") &&
        name.size() > firstWord.size() &&
        name.substr(0, firstWord.size()) == firstWord) {
        name = name.substr(firstWord.size());
    }

    return name;
}

// ── Game type classifier ──────────────────────────────────────────────────────

static std::string classifyGameType(const std::vector<ZipEntry>& entries) {
    for (size_t i = 0; i < entries.size(); i++) {
        const std::string& ext = entries[i].ext;
        if (ext == "ISO" || ext == "CUE" || ext == "BIN" || ext == "MDF")
            return "CD_BASED";
    }
    for (size_t i = 0; i < entries.size(); i++) {
        if (entries[i].ext == "BAT") {
            std::string lower = toLower(entries[i].base);
            if (lower == "start.bat" || lower == "run.bat" || lower == "go.bat")
                return "BATCH_LAUNCHER";
        }
    }
    return entries.size() > 50 ? "COMPLEX" : "SIMPLE";
}

// ── Exe scorer ────────────────────────────────────────────────────────────────

static float scoreExe(const ZipEntry& e, const std::string& zipBase, size_t maxCompSize) {
    std::string stem = toLower(stemOf(e.base));
    if (isBlacklisted(stem)) return 0.0f;

    float score = 0.0f;
    if      (e.ext == "EXE") score = 1.0f;
    else if (e.ext == "COM") score = 0.6f;
    else if (e.ext == "BAT") score = 0.7f;
    else return 0.0f;

    score -= e.depth * 0.15f;
    if (score < 0.01f) score = 0.01f;

    std::string zipStem = toLower(stemOf(zipBase));
    if (stem == zipStem || stem.find(zipStem) == 0 || zipStem.find(stem) == 0)
        score += 0.3f;

    if (stem == "game" || stem == "play" || stem == "start" ||
        stem == "run"  || stem == "main" || stem == "go")
        score += 0.15f;

    if (maxCompSize > 0)
        score += ((float)e.compSize / (float)maxCompSize) * 0.25f;

    return score < 1.5f ? score : 1.5f;
}

// ── Database loader ───────────────────────────────────────────────────────────

static json loadDatabase(const std::string& dbPath) {
    std::ifstream f(dbPath.c_str());
    if (!f.is_open()) return json::object();
    json data;
    try { f >> data; return data.value("games", json::object()); }
    catch (...) { return json::object(); }
}

// ── Find ISO ──────────────────────────────────────────────────────────────────

static std::string findIsoInDir(const std::string& dir) {
    WIN32_FIND_DATAA fd = {};
    std::string pattern = dir + "\\*";
    HANDLE h = FindFirstFileA(pattern.c_str(), &fd);
    if (h == INVALID_HANDLE_VALUE) return "";
    std::string found;
    do {
        std::string name = fd.cFileName;
        if (name == "." || name == "..") continue;
        std::string full = dir + "\\" + name;
        if (fd.dwFileAttributes & FILE_ATTRIBUTE_DIRECTORY) {
            found = findIsoInDir(full);
            if (!found.empty()) break;
        } else {
            std::string ext = toUpper(extOf(name));
            if (ext == "ISO" || ext == "CUE" || ext == "BIN" || ext == "MDF") {
                found = full; break;
            }
        }
    } while (FindNextFileA(h, &fd));
    FindClose(h);
    return found;
}

// ── Analyze ───────────────────────────────────────────────────────────────────

AnalyzeResult analyze(const std::string& zipPath, const std::string& dbPath) {
    AnalyzeResult result;
    auto entries = readZipEntries(zipPath);
    if (entries.empty()) { result.error = "Zip is empty or unreadable"; return result; }

    std::string fp = fingerprint(zipPath);
    std::string gt = classifyGameType(entries);
    result.gameType = gt;

    json db = loadDatabase(dbPath);
    json dbEntry;
    if (db.contains(fp)) {
        dbEntry = db[fp];
    } else {
        for (json::iterator it = db.begin(); it != db.end(); ++it) {
            if (fp.find(it.key()) != std::string::npos) { dbEntry = it.value(); break; }
        }
    }

    if (!dbEntry.is_null()) {
        std::string exeName = toUpper(dbEntry.value("exe", ""));
        for (size_t i = 0; i < entries.size(); i++) {
            if (entries[i].base == exeName) {
                result.success    = true;
                result.exe        = entries[i].name;
                result.workDir    = dbEntry.value("work_dir", "");
                result.source     = "database";
                result.confidence = 1.0f;
                result.title      = dbEntry.value("title", "");
                if (dbEntry.contains("cycles")) {
                    json& cyc = dbEntry["cycles"];
                    if (cyc.is_string())      result.cycles = cyc.get<std::string>();
                    else if (cyc.is_number()) result.cycles = std::to_string(cyc.get<int>());
                    else                      result.cycles = "max limit 80000";
                } else result.cycles = "max limit 80000";
                result.memsize = dbEntry.value("memsize", 16);
                result.ems     = dbEntry.value("ems", true);
                result.xms     = dbEntry.value("xms", true);
                result.cdMount = dbEntry.value("cd_mount", false);
                return result;
            }
        }
    }

    // Batch launcher
    if (gt == "BATCH_LAUNCHER") {
        for (size_t i = 0; i < entries.size(); i++) {
            if (entries[i].ext == "BAT") {
                std::string lower = toLower(entries[i].base);
                if (lower == "start.bat" || lower == "run.bat" || lower == "go.bat") {
                    result.success    = true;
                    result.exe        = entries[i].name;
                    result.workDir    = dirOf(entries[i].name);
                    result.source     = "batch";
                    result.confidence = 0.85f;
                    return result;
                }
            }
        }
    }

    // Scorer
    std::vector<ZipEntry> exeEntries;
    for (size_t i = 0; i < entries.size(); i++) {
        const std::string& ext = entries[i].ext;
        if (ext == "EXE" || ext == "COM" || ext == "BAT")
            exeEntries.push_back(entries[i]);
    }

    size_t maxComp = 0;
    for (size_t i = 0; i < exeEntries.size(); i++)
        if (exeEntries[i].compSize > maxComp) maxComp = exeEntries[i].compSize;

    std::string zipBase = basename(zipPath);
    std::vector<std::pair<float, ZipEntry>> scored;
    for (size_t i = 0; i < exeEntries.size(); i++) {
        float s = scoreExe(exeEntries[i], zipBase, maxComp);
        if (s > 0.0f) scored.push_back(std::make_pair(s, exeEntries[i]));
    }

    if (scored.empty()) { result.error = "No executable files found"; return result; }

    for (size_t i = 0; i < scored.size(); i++)
        for (size_t j = i+1; j < scored.size(); j++)
            if (scored[j].first > scored[i].first) std::swap(scored[i], scored[j]);

    result.success    = true;
    result.exe        = scored[0].second.name;
    result.workDir    = dirOf(scored[0].second.name);
    result.source     = "scored";
    result.confidence = scored[0].first / 1.5f < 1.0f ? scored[0].first / 1.5f : 1.0f;
    if (gt == "CD_BASED") result.cdMount = true;
    return result;
}

// ── Extract zip ───────────────────────────────────────────────────────────────

bool extractZip(const std::string& zipPath, const std::string& outDir) {
    mz_zip_archive zip = {};
    if (!mz_zip_reader_init_file(&zip, zipPath.c_str(), 0)) return false;

    int count = (int)mz_zip_reader_get_num_files(&zip);
    for (int i = 0; i < count; i++) {
        if (mz_zip_reader_is_file_a_directory(&zip, i)) continue;
        mz_zip_archive_file_stat stat = {};
        if (!mz_zip_reader_file_stat(&zip, i, &stat)) continue;

        std::string name = stat.m_filename;
        std::replace(name.begin(), name.end(), '/', '\\');
        if (name.find("..\\") != std::string::npos) continue;
        if (name.size() > 1 && name[1] == ':') continue;
        if (name.empty()) continue;

        std::string outPath = outDir + "\\" + name;
        std::string dir = outPath.substr(0, outPath.rfind('\\'));
        for (size_t pos = outDir.size(); pos < dir.size(); ) {
            pos = dir.find('\\', pos + 1);
            if (pos == std::string::npos) pos = dir.size();
            CreateDirectoryA(dir.substr(0, pos).c_str(), nullptr);
        }
        mz_zip_reader_extract_to_file(&zip, i, outPath.c_str(), 0);
    }

    mz_zip_reader_end(&zip);
    return true;
}

// ── Write DOSBox conf ─────────────────────────────────────────────────────────

bool writeDosboxConf(const std::string& zipPath,
                     const std::string& extractedDir,
                     const AnalyzeResult& result) {
    std::string confPath = zipPath.substr(0, zipPath.rfind('.')) + ".conf";

    std::string exeFull = result.exe;
    std::replace(exeFull.begin(), exeFull.end(), '/', '\\');
    size_t lastSlash = exeFull.rfind('\\');
    std::string exeName   = (lastSlash != std::string::npos) ? exeFull.substr(lastSlash+1) : exeFull;
    std::string exeSubDir = (lastSlash != std::string::npos) ? exeFull.substr(0, lastSlash) : "";
    std::string cdDir     = result.workDir.empty() ? exeSubDir : result.workDir;
    std::string cycles    = result.cycles.empty() ? "max limit 80000" : result.cycles;
    int         memsize   = result.memsize > 0 ? result.memsize : 16;

    std::ostringstream autoexec;
    autoexec << "@echo off\r\n";
    autoexec << "mount C \"" << extractedDir << "\"\r\n";
    if (result.cdMount) {
        std::string iso = findIsoInDir(extractedDir);
        if (!iso.empty()) autoexec << "imgmount D \"" << iso << "\" -t iso\r\n";
    }
    autoexec << "C:\r\n";
    if (!cdDir.empty()) autoexec << "cd \\" << cdDir << "\r\n";
    autoexec << exeName << "\r\n";
    autoexec << "exit\r\n";

    std::ostringstream conf;
    conf << "[sdl]\r\nfullscreen=true\r\nfullresolution=desktop\r\noutput=openglnb\r\n\r\n";
    conf << "[dosbox]\r\nmachine=svga_s3\r\nmemsize=" << memsize << "\r\n\r\n";
    conf << "[cpu]\r\ncore=dynamic\r\ncputype=pentium_slow\r\ncycles=" << cycles << "\r\ncycleup=500\r\ncycledown=20\r\n\r\n";
    conf << "[dos]\r\nems=" << (result.ems?"true":"false") << "\r\nxms=" << (result.xms?"true":"false") << "\r\n\r\n";
    conf << "[mixer]\r\nrate=44100\r\nblocksize=1024\r\nprebuffer=20\r\n\r\n";
    conf << "[render]\r\nframeskip=0\r\naspect=true\r\n\r\n";
    conf << "[autoexec]\r\n" << autoexec.str() << "\r\n";

    std::ofstream f(confPath.c_str());
    if (!f.is_open()) return false;
    f << conf.str();
    return true;
}

// ── Launch DOSBox ─────────────────────────────────────────────────────────────

bool launchDosBox(const std::string& dosboxPath, const std::string& confPath) {
    std::string cmd = "\"" + dosboxPath + "\" -conf \"" + confPath + "\"";
    STARTUPINFOA        si = { sizeof(si) };
    PROCESS_INFORMATION pi = {};
    bool ok = CreateProcessA(nullptr, const_cast<char*>(cmd.c_str()),
        nullptr, nullptr, FALSE, DETACHED_PROCESS, nullptr, nullptr, &si, &pi);
    if (ok) { CloseHandle(pi.hProcess); CloseHandle(pi.hThread); }
    return ok;
}

// ── Add to database ───────────────────────────────────────────────────────────

bool addToDatabase(const std::string& dbPath, const AnalyzeResult& result) {
    json data;
    std::ifstream fin(dbPath.c_str());
    if (fin.is_open()) { try { fin >> data; } catch (...) {} fin.close(); }

    std::string key = fingerprint(result.title.empty() ? result.exe : result.title);
    if (key.empty()) return false;

    json& games = data["games"];
    if (games.contains(key) && games[key].value("source","") == "manual") return false;

    games[key] = {
        {"title",         result.title},
        {"exe",           basename(result.exe)},
        {"cycles",        result.cycles.empty() ? "max limit 80000" : result.cycles},
        {"memsize",       result.memsize},
        {"ems",           result.ems},
        {"xms",           result.xms},
        {"cd_mount",      result.cdMount},
        {"work_dir",      result.workDir},
        {"install_first", false},
        {"source",        "autosync"},
    };
    data["_meta"]["games"] = games.size();

    std::ofstream fout(dbPath.c_str());
    if (!fout.is_open()) return false;
    fout << data.dump(2);
    return true;
}

} // namespace AutoDOS
