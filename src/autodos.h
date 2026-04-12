#pragma once
// autodos.h — AutoDOS32 core library (Windows XP compatible)
// No std::filesystem, no std::thread, no C++17

#include <string>
#include <vector>
#include <windows.h>

namespace AutoDOS {

struct AnalyzeResult {
    bool        success    = false;
    std::string exe;
    std::string workDir;
    std::string gameType;
    std::string source;
    float       confidence = 0.0f;
    std::string error;
    std::string title;
    std::string cycles;
    int         memsize    = 16;
    bool        ems        = true;
    bool        xms        = true;
    bool        cdMount    = false;
};

struct GameEntry {
    std::string id;
    std::string title;
    std::string zipPath;
    std::string confPath;
    std::string source;
    float       confidence = 0.0f;
};

AnalyzeResult analyze(const std::string& zipPath, const std::string& dbPath);
bool          extractZip(const std::string& zipPath, const std::string& outDir);
bool          writeDosboxConf(const std::string& zipPath, const std::string& extractedDir, const AnalyzeResult& result);
bool          launchDosBox(const std::string& dosboxPath, const std::string& confPath);
std::string   fingerprint(const std::string& filename);
bool          addToDatabase(const std::string& dbPath, const AnalyzeResult& result);

// Win32 filesystem helpers (replaces std::filesystem)
bool          pathExists(const std::string& path);
bool          createDirs(const std::string& path);
std::string   pathJoin(const std::string& a, const std::string& b);
std::string   pathStem(const std::string& path);
std::string   pathFilename(const std::string& path);

} // namespace AutoDOS
