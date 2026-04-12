// main.cpp — AutoDOS32 GUI (Windows XP compatible)
// No std::filesystem, no std::thread, no std::atomic
// Uses CreateThread, Win32 file APIs throughout

#include <windows.h>
#include <windowsx.h>
#include <commctrl.h>
#include <shellapi.h>
#include <shlobj.h>
#include <commdlg.h>
#include <string>
#include <vector>
#include <fstream>
#include <algorithm>
#include <sstream>

#include "autodos.h"
#include "nlohmann/json.hpp"

#pragma comment(lib, "comctl32.lib")
#pragma comment(lib, "shell32.lib")
#pragma comment(lib, "comdlg32.lib")

using json = nlohmann::json;

// ── IDs ───────────────────────────────────────────────────────────────────────
#define IDC_LIST        1001
#define IDC_BTN_LAUNCH  1002
#define IDC_BTN_DELETE  1003
#define IDC_BTN_ADD     1004
#define IDC_STATUS      1005
#define IDM_LAUNCH      2001
#define IDM_DELETE      2002
#define WM_IMPORT_DONE  (WM_APP + 1)
#define WM_SET_STATUS   (WM_APP + 2)

// ── Colors ────────────────────────────────────────────────────────────────────
#define CLR_BG        RGB(18,  18,  24)
#define CLR_ITEM      RGB(28,  28,  36)
#define CLR_ITEM_SEL  RGB(32,  52,  40)
#define CLR_ACCENT    RGB(80,  200, 120)
#define CLR_TEXT      RGB(220, 220, 220)
#define CLR_TEXT_DIM  RGB(110, 110, 120)
#define CLR_DIVIDER   RGB(38,  38,  50)

// ── Structs ───────────────────────────────────────────────────────────────────

struct LibEntry {
    std::string id;
    std::string title;
    std::string zipPath;
    std::string confPath;
    std::string source;
    float       confidence;
    LibEntry() : confidence(0.0f) {}
};

struct ImportResult {
    bool        ok;
    std::string error;
    LibEntry    entry;
    AutoDOS::AnalyzeResult analyzeResult;
    ImportResult() : ok(false) {}
};

struct ThreadParam {
    std::string zipPath;
    HWND        hwnd;
};

// ── Globals ───────────────────────────────────────────────────────────────────
static HWND g_hwnd      = NULL;
static HWND g_list      = NULL;
static HWND g_status    = NULL;
static HWND g_btnLaunch = NULL;
static HWND g_btnDelete = NULL;
static HWND g_btnAdd    = NULL;

static std::string g_appDir;
static std::string g_dbPath;
static std::string g_libPath;
static std::string g_dosboxPath;

static std::vector<LibEntry> g_library;
static CRITICAL_SECTION      g_cs;
static bool                  g_working = false;
static std::vector<std::string> g_queue;

static HBRUSH g_hbrBg    = NULL;
static HFONT  g_fontItem = NULL;
static HFONT  g_fontSm   = NULL;

// ── Path helpers ──────────────────────────────────────────────────────────────

static std::string getAppDataDir() {
    char p[MAX_PATH];
    SHGetFolderPathA(NULL, CSIDL_APPDATA, NULL, 0, p);
    return std::string(p) + "\\AutoDOS";
}

static std::string getExeDir() {
    char p[MAX_PATH];
    GetModuleFileNameA(NULL, p, MAX_PATH);
    std::string s = p;
    return s.substr(0, s.rfind('\\'));
}

static std::string makeId() {
    static int n = 0;
    char buf[64];
    wsprintfA(buf, "g%lu_%d", GetTickCount(), n++);
    return std::string(buf);
}

// ── Thread-safe status ────────────────────────────────────────────────────────

static void postStatus(const std::string& msg) {
    char* copy = new char[msg.size() + 1];
    lstrcpyA(copy, msg.c_str());
    PostMessageA(g_hwnd, WM_SET_STATUS, 0, (LPARAM)copy);
}

// ── Library IO ────────────────────────────────────────────────────────────────

static void saveLibrary() {
    json arr = json::array();
    for (size_t i = 0; i < g_library.size(); i++) {
        const LibEntry& e = g_library[i];
        arr.push_back({{"id",e.id},{"title",e.title},
                       {"zipPath",e.zipPath},{"confPath",e.confPath},
                       {"source",e.source},{"confidence",e.confidence}});
    }
    std::ofstream f(g_libPath.c_str());
    if (f.is_open()) f << arr.dump(2);
}

static void loadLibrary() {
    g_library.clear();
    std::ifstream f(g_libPath.c_str());
    if (!f.is_open()) return;
    try {
        json arr; f >> arr;
        for (size_t i = 0; i < arr.size(); i++) {
            LibEntry e;
            e.id         = arr[i].value("id","");
            e.title      = arr[i].value("title","");
            e.zipPath    = arr[i].value("zipPath","");
            e.confPath   = arr[i].value("confPath","");
            e.source     = arr[i].value("source","");
            e.confidence = arr[i].value("confidence",0.0f);
            if (!e.id.empty()) g_library.push_back(e);
        }
    } catch(...) {}
}

// ── UI helpers ────────────────────────────────────────────────────────────────

static void setStatus(const std::string& msg) {
    SetWindowTextA(g_status, msg.c_str());
}

static void refreshList() {
    SendMessage(g_list, LB_RESETCONTENT, 0, 0);
    for (size_t i = 0; i < g_library.size(); i++) {
        std::string label = g_library[i].title;
        if (g_library[i].source == "scored") {
            char buf[32];
            wsprintfA(buf, "  [%d%%]", (int)(g_library[i].confidence * 100));
            label += buf;
        }
        SendMessageA(g_list, LB_ADDSTRING, 0, (LPARAM)label.c_str());
    }
    bool has = SendMessage(g_list, LB_GETCURSEL, 0, 0) != LB_ERR;
    EnableWindow(g_btnLaunch, has ? TRUE : FALSE);
    EnableWindow(g_btnDelete, has ? TRUE : FALSE);
}

// ── Worker thread ─────────────────────────────────────────────────────────────

static DWORD WINAPI workerThread(LPVOID param) {
    ThreadParam* tp = (ThreadParam*)param;
    std::string zipPath = tp->zipPath;
    HWND hwnd = tp->hwnd;
    delete tp;

    ImportResult* res = new ImportResult();

    try {
        postStatus("Analyzing: " + AutoDOS::pathFilename(zipPath) + "...");

        res->analyzeResult = AutoDOS::analyze(zipPath, g_dbPath);
        if (!res->analyzeResult.success) {
            res->ok    = false;
            res->error = res->analyzeResult.error.empty()
                         ? "Could not identify game executable"
                         : res->analyzeResult.error;
            PostMessageA(hwnd, WM_IMPORT_DONE, 0, (LPARAM)res);
            return 0;
        }

        std::string stem    = AutoDOS::pathStem(zipPath);
        std::string gameDir = AutoDOS::pathJoin(g_appDir, "games\\" + stem);
        AutoDOS::createDirs(gameDir);

        postStatus("Extracting: " + stem + "...");
        AutoDOS::extractZip(zipPath, gameDir);

        std::string confPath = AutoDOS::pathJoin(g_appDir, "games\\" + stem + ".conf");
        AutoDOS::writeDosboxConf(zipPath, gameDir, res->analyzeResult);

        // Move temp conf if written next to zip
        std::string tempConf = zipPath.substr(0, zipPath.rfind('.')) + ".conf";
        if (AutoDOS::pathExists(tempConf)) {
            CopyFileA(tempConf.c_str(), confPath.c_str(), FALSE);
            DeleteFileA(tempConf.c_str());
        }

        std::string title = res->analyzeResult.title.empty()
                            ? stem : res->analyzeResult.title;

        res->ok               = true;
        res->entry.id         = makeId();
        res->entry.title      = title;
        res->entry.zipPath    = zipPath;
        res->entry.confPath   = confPath;
        res->entry.source     = res->analyzeResult.source;
        res->entry.confidence = res->analyzeResult.confidence;

    } catch(...) {
        res->ok    = false;
        res->error = "Unexpected error during import";
    }

    PostMessageA(hwnd, WM_IMPORT_DONE, 0, (LPARAM)res);
    return 0;
}

static void startNextJob() {
    EnterCriticalSection(&g_cs);
    if (g_queue.empty()) {
        g_working = false;
        LeaveCriticalSection(&g_cs);
        return;
    }
    std::string next = g_queue[0];
    g_queue.erase(g_queue.begin());
    LeaveCriticalSection(&g_cs);

    ThreadParam* tp = new ThreadParam();
    tp->zipPath = next;
    tp->hwnd    = g_hwnd;
    HANDLE h = CreateThread(NULL, 0, workerThread, tp, 0, NULL);
    if (h) CloseHandle(h);
}

static void enqueueZip(const std::string& zipPath) {
    // Duplicate check
    for (size_t i = 0; i < g_library.size(); i++) {
        if (g_library[i].zipPath == zipPath) {
            setStatus("Already in library: " + g_library[i].title);
            return;
        }
    }

    EnterCriticalSection(&g_cs);
    if (g_working) {
        g_queue.push_back(zipPath);
        LeaveCriticalSection(&g_cs);
        setStatus("Queued: " + AutoDOS::pathFilename(zipPath));
        return;
    }
    g_working = true;
    LeaveCriticalSection(&g_cs);

    ThreadParam* tp = new ThreadParam();
    tp->zipPath = zipPath;
    tp->hwnd    = g_hwnd;
    HANDLE h = CreateThread(NULL, 0, workerThread, tp, 0, NULL);
    if (h) CloseHandle(h);
}

// ── Launch / Delete ───────────────────────────────────────────────────────────

static void launchSelected() {
    int idx = (int)SendMessage(g_list, LB_GETCURSEL, 0, 0);
    if (idx < 0 || idx >= (int)g_library.size()) return;
    const LibEntry& e = g_library[idx];
    if (!AutoDOS::pathExists(e.confPath)) { setStatus("Conf missing - re-import"); return; }
    if (!AutoDOS::launchDosBox(g_dosboxPath, e.confPath)) { setStatus("Failed to launch DOSBox"); return; }
    setStatus("Launching: " + e.title);
}

static void deleteSelected() {
    int idx = (int)SendMessage(g_list, LB_GETCURSEL, 0, 0);
    if (idx < 0 || idx >= (int)g_library.size()) return;
    std::string title    = g_library[idx].title;
    std::string confPath = g_library[idx].confPath;
    std::string prompt   = "Remove \"" + title + "\" from library?";
    if (MessageBoxA(g_hwnd, prompt.c_str(), "AutoDOS", MB_YESNO|MB_ICONQUESTION) != IDYES) return;
    DeleteFileA(confPath.c_str());
    // Remove game folder
    std::string gameDir = confPath.substr(0, confPath.rfind('.'));
    // Simple recursive delete via SHFileOperation
    SHFILEOPSTRUCTA op = {};
    char from[MAX_PATH+1] = {};
    lstrcpyA(from, gameDir.c_str());
    op.wFunc  = FO_DELETE;
    op.pFrom  = from;
    op.fFlags = FOF_NOCONFIRMATION | FOF_SILENT | FOF_NOERRORUI;
    SHFileOperationA(&op);

    g_library.erase(g_library.begin() + idx);
    saveLibrary();
    refreshList();
    setStatus("Removed: " + title);
}

static void browseAndAdd() {
    char path[MAX_PATH] = {};
    OPENFILENAMEA ofn   = {};
    ofn.lStructSize = sizeof(ofn);
    ofn.hwndOwner   = g_hwnd;
    ofn.lpstrFilter = "DOS Game Archives\0*.zip;*.7z;*.rar\0All Files\0*.*\0";
    ofn.lpstrFile   = path;
    ofn.nMaxFile    = MAX_PATH;
    ofn.Flags       = OFN_FILEMUSTEXIST|OFN_PATHMUSTEXIST;
    ofn.lpstrTitle  = "Select DOS Game Zip";
    if (GetOpenFileNameA(&ofn)) enqueueZip(path);
}

// ── Owner-draw list ───────────────────────────────────────────────────────────

static void drawItem(DRAWITEMSTRUCT* dis) {
    if (dis->itemID == (UINT)-1) return;
    HDC dc  = dis->hDC;
    RECT rc = dis->rcItem;
    bool sel = (dis->itemState & ODS_SELECTED) != 0;

    HBRUSH hbr = CreateSolidBrush(sel ? CLR_ITEM_SEL : CLR_ITEM);
    FillRect(dc, &rc, hbr); DeleteObject(hbr);

    if (sel) {
        HBRUSH ab = CreateSolidBrush(CLR_ACCENT);
        RECT bar  = {rc.left, rc.top, rc.left+3, rc.bottom};
        FillRect(dc, &bar, ab); DeleteObject(ab);
    }

    char text[256] = {};
    SendMessageA(dis->hwndItem, LB_GETTEXT, dis->itemID, (LPARAM)text);
    SetBkMode(dc, TRANSPARENT);
    SetTextColor(dc, sel ? CLR_ACCENT : CLR_TEXT);
    SelectObject(dc, g_fontItem);
    RECT tr = {rc.left+14, rc.top, rc.right-10, rc.bottom};
    DrawTextA(dc, text, -1, &tr, DT_SINGLELINE|DT_VCENTER|DT_END_ELLIPSIS);

    HPEN pen = CreatePen(PS_SOLID, 1, CLR_DIVIDER);
    SelectObject(dc, pen);
    MoveToEx(dc, rc.left, rc.bottom-1, NULL);
    LineTo(dc, rc.right, rc.bottom-1);
    DeleteObject(pen);
}

// ── WndProc ───────────────────────────────────────────────────────────────────

static LRESULT CALLBACK WndProc(HWND hwnd, UINT msg, WPARAM wParam, LPARAM lParam) {
    switch (msg) {

    case WM_CREATE:
        DragAcceptFiles(hwnd, TRUE);
        return 0;

    case WM_SIZE: {
        int W=LOWORD(lParam), H=HIWORD(lParam);
        int pad=10, btnH=32, btnW=90, barH=28;
        int listH = H - btnH - barH - pad*3;
        SetWindowPos(g_list,      NULL, pad,        pad,   W-pad*2, listH, SWP_NOZORDER);
        int btnY = pad + listH + pad;
        SetWindowPos(g_btnLaunch, NULL, pad,        btnY,  btnW, btnH, SWP_NOZORDER);
        SetWindowPos(g_btnAdd,    NULL, pad+btnW+8, btnY,  btnW, btnH, SWP_NOZORDER);
        SetWindowPos(g_btnDelete, NULL, W-btnW-pad, btnY,  btnW, btnH, SWP_NOZORDER);
        SetWindowPos(g_status,    NULL, 0, H-barH,  W,    barH, SWP_NOZORDER);
        return 0;
    }

    case WM_DROPFILES: {
        HDROP drop = (HDROP)wParam;
        UINT count = DragQueryFileA(drop, 0xFFFFFFFF, NULL, 0);
        for (UINT i = 0; i < count; i++) {
            char path[MAX_PATH];
            DragQueryFileA(drop, i, path, MAX_PATH);
            std::string p = path;
            if (p.rfind('.') == std::string::npos) continue;
            std::string ext = p.substr(p.rfind('.')+1);
            std::transform(ext.begin(), ext.end(), ext.begin(), ::tolower);
            if (ext=="zip"||ext=="7z"||ext=="rar") enqueueZip(p);
        }
        DragFinish(drop);
        return 0;
    }

    case WM_IMPORT_DONE: {
        ImportResult* res = (ImportResult*)lParam;
        if (!res) { startNextJob(); return 0; }

        if (!res->ok) {
            setStatus("Error: " + res->error);
        } else {
            bool dup = false;
            for (size_t i = 0; i < g_library.size(); i++)
                if (g_library[i].zipPath == res->entry.zipPath) { dup = true; break; }

            if (!dup) {
                g_library.push_back(res->entry);
                saveLibrary();

                if (res->analyzeResult.source == "scored") {
                    res->analyzeResult.title = res->entry.title;
                    AutoDOS::addToDatabase(g_dbPath, res->analyzeResult);
                }

                refreshList();
                SendMessage(g_list, LB_SETCURSEL, g_library.size()-1, 0);
                EnableWindow(g_btnLaunch, TRUE);
                EnableWindow(g_btnDelete, TRUE);

                std::string src = (res->entry.source == "database") ? "DB"
                    : "Auto " + std::to_string((int)(res->entry.confidence*100)) + "%";
                setStatus("Added: " + res->entry.title + "  [" + src + "]");
            } else {
                setStatus("Already in library: " + res->entry.title);
            }
        }

        delete res;
        startNextJob();
        return 0;
    }

    case WM_SET_STATUS: {
        char* m = (char*)lParam;
        if (m) { setStatus(m); delete[] m; }
        return 0;
    }

    case WM_COMMAND: {
        int id = LOWORD(wParam);
        if (id==IDC_BTN_LAUNCH||id==IDM_LAUNCH)       { launchSelected(); return 0; }
        if (id==IDC_BTN_DELETE||id==IDM_DELETE)       { deleteSelected(); return 0; }
        if (id==IDC_BTN_ADD)                           { browseAndAdd();   return 0; }
        if (id==IDC_LIST&&HIWORD(wParam)==LBN_DBLCLK) { launchSelected(); return 0; }
        if (id==IDC_LIST&&HIWORD(wParam)==LBN_SELCHANGE) {
            bool has = SendMessage(g_list,LB_GETCURSEL,0,0) != LB_ERR;
            EnableWindow(g_btnLaunch, has?TRUE:FALSE);
            EnableWindow(g_btnDelete, has?TRUE:FALSE);
        }
        return 0;
    }

    case WM_MEASUREITEM:
        ((MEASUREITEMSTRUCT*)lParam)->itemHeight = 40;
        return TRUE;

    case WM_DRAWITEM: {
        DRAWITEMSTRUCT* dis = (DRAWITEMSTRUCT*)lParam;
        if (dis->CtlID == IDC_LIST) drawItem(dis);
        return TRUE;
    }

    case WM_CTLCOLORLISTBOX:
    case WM_CTLCOLORSTATIC:
    case WM_CTLCOLORBTN:
        SetBkColor((HDC)wParam, CLR_BG);
        SetTextColor((HDC)wParam, CLR_TEXT_DIM);
        return (LRESULT)g_hbrBg;

    case WM_ERASEBKGND: {
        RECT rc; GetClientRect(hwnd, &rc);
        FillRect((HDC)wParam, &rc, g_hbrBg);
        return 1;
    }

    case WM_CONTEXTMENU:
        if ((HWND)wParam == g_list) {
            HMENU m = CreatePopupMenu();
            AppendMenuA(m, MF_STRING, IDM_LAUNCH, "Launch");
            AppendMenuA(m, MF_STRING, IDM_DELETE, "Remove");
            TrackPopupMenu(m, TPM_RIGHTBUTTON,
                GET_X_LPARAM(lParam), GET_Y_LPARAM(lParam), 0, hwnd, NULL);
            DestroyMenu(m);
        }
        return 0;

    case WM_DESTROY:
        DeleteCriticalSection(&g_cs);
        PostQuitMessage(0);
        return 0;
    }
    return DefWindowProcA(hwnd, msg, wParam, lParam);
}

// ── WinMain ───────────────────────────────────────────────────────────────────

int WINAPI WinMain(HINSTANCE hInst, HINSTANCE, LPSTR, int nCmdShow) {
    InitializeCriticalSection(&g_cs);

    INITCOMMONCONTROLSEX icc = {sizeof(icc), ICC_WIN95_CLASSES};
    InitCommonControlsEx(&icc);

    g_appDir     = getAppDataDir();
    g_dbPath     = AutoDOS::pathJoin(g_appDir, "games.json");
    g_libPath    = AutoDOS::pathJoin(g_appDir, "library.json");
    g_dosboxPath = AutoDOS::pathJoin(getExeDir(), "dosbox\\dosbox.exe");

    AutoDOS::createDirs(g_appDir);
    AutoDOS::createDirs(AutoDOS::pathJoin(g_appDir, "games"));

    if (!AutoDOS::pathExists(g_dbPath)) {
        std::string src = AutoDOS::pathJoin(getExeDir(), "games.json");
        if (AutoDOS::pathExists(src)) CopyFileA(src.c_str(), g_dbPath.c_str(), FALSE);
    }

    loadLibrary();

    g_hbrBg   = CreateSolidBrush(CLR_BG);
    g_fontItem = CreateFontA(15,0,0,0,FW_NORMAL,0,0,0,DEFAULT_CHARSET,0,0,CLEARTYPE_QUALITY,0,"Tahoma");
    g_fontSm   = CreateFontA(12,0,0,0,FW_NORMAL,0,0,0,DEFAULT_CHARSET,0,0,CLEARTYPE_QUALITY,0,"Tahoma");

    WNDCLASSEXA wc   = {sizeof(wc)};
    wc.style         = CS_HREDRAW|CS_VREDRAW;
    wc.lpfnWndProc   = WndProc;
    wc.hInstance     = hInst;
    wc.hbrBackground = g_hbrBg;
    wc.lpszClassName = "AutoDOS32_Main";
    wc.hCursor       = LoadCursor(NULL, IDC_ARROW);
    wc.hIcon         = (HICON)LoadImageA(hInst, "assets\\icon.ico", IMAGE_ICON, 32, 32, LR_LOADFROMFILE);
    wc.hIconSm       = (HICON)LoadImageA(hInst, "assets\\icon.ico", IMAGE_ICON, 16, 16, LR_LOADFROMFILE);
    RegisterClassExA(&wc);

    g_hwnd = CreateWindowExA(WS_EX_ACCEPTFILES,
        "AutoDOS32_Main", "AutoDOS",
        WS_OVERLAPPEDWINDOW,
        CW_USEDEFAULT, CW_USEDEFAULT, 500, 600,
        NULL, NULL, hInst, NULL);

    // Set icons on window
    HICON hIconBig = (HICON)LoadImageA(hInst, "assets\\icon.ico", IMAGE_ICON, 32, 32, LR_LOADFROMFILE);
    HICON hIconSml = (HICON)LoadImageA(hInst, "assets\\icon.ico", IMAGE_ICON, 16, 16, LR_LOADFROMFILE);
    if (hIconBig) SendMessageA(g_hwnd, WM_SETICON, ICON_BIG,   (LPARAM)hIconBig);
    if (hIconSml) SendMessageA(g_hwnd, WM_SETICON, ICON_SMALL, (LPARAM)hIconSml);

    g_list = CreateWindowExA(WS_EX_CLIENTEDGE, "LISTBOX", NULL,
        WS_CHILD|WS_VISIBLE|WS_VSCROLL|LBS_NOTIFY|LBS_OWNERDRAWFIXED|LBS_HASSTRINGS,
        0,0,0,0, g_hwnd, (HMENU)IDC_LIST, hInst, NULL);
    SendMessage(g_list, WM_SETFONT, (WPARAM)g_fontItem, TRUE);

    g_btnLaunch = CreateWindowA("BUTTON","Launch",WS_CHILD|WS_VISIBLE|BS_PUSHBUTTON,
        0,0,0,0, g_hwnd, (HMENU)IDC_BTN_LAUNCH, hInst, NULL);
    SendMessage(g_btnLaunch, WM_SETFONT, (WPARAM)g_fontItem, TRUE);
    EnableWindow(g_btnLaunch, FALSE);

    g_btnAdd = CreateWindowA("BUTTON","Add Zip",WS_CHILD|WS_VISIBLE|BS_PUSHBUTTON,
        0,0,0,0, g_hwnd, (HMENU)IDC_BTN_ADD, hInst, NULL);
    SendMessage(g_btnAdd, WM_SETFONT, (WPARAM)g_fontItem, TRUE);

    g_btnDelete = CreateWindowA("BUTTON","Remove",WS_CHILD|WS_VISIBLE|BS_PUSHBUTTON,
        0,0,0,0, g_hwnd, (HMENU)IDC_BTN_DELETE, hInst, NULL);
    SendMessage(g_btnDelete, WM_SETFONT, (WPARAM)g_fontItem, TRUE);
    EnableWindow(g_btnDelete, FALSE);

    g_status = CreateWindowA("STATIC",
        "Drop a DOS zip to add  |  Double-click to launch",
        WS_CHILD|WS_VISIBLE|SS_LEFT,
        0,0,0,0, g_hwnd, (HMENU)IDC_STATUS, hInst, NULL);
    SendMessage(g_status, WM_SETFONT, (WPARAM)g_fontSm, TRUE);

    refreshList();
    ShowWindow(g_hwnd, nCmdShow);
    UpdateWindow(g_hwnd);

    MSG msg;
    while (GetMessage(&msg, NULL, 0, 0)) {
        TranslateMessage(&msg);
        DispatchMessage(&msg);
    }

    DeleteObject(g_hbrBg);
    DeleteObject(g_fontItem);
    DeleteObject(g_fontSm);
    return (int)msg.wParam;
}
