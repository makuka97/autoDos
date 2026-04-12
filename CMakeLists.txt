cmake_minimum_required(VERSION 3.20)
project(AutoDOS32 VERSION 1.0.0 LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 14)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_POLICY_VERSION_MINIMUM 3.5)

set(CMAKE_RUNTIME_OUTPUT_DIRECTORY ${CMAKE_BINARY_DIR}/bin)

# ── nlohmann/json ─────────────────────────────────────────────────────────────
include(FetchContent)
FetchContent_Declare(
    nlohmann_json
    GIT_REPOSITORY https://github.com/nlohmann/json.git
    GIT_TAG        v3.11.3
)
FetchContent_MakeAvailable(nlohmann_json)

# ── Sources ───────────────────────────────────────────────────────────────────
add_executable(AutoDOS32 WIN32
    src/main.cpp
    src/autodos.cpp
    src/miniz.c
    assets/icon.rc
)

target_include_directories(AutoDOS32 PRIVATE src)

target_link_libraries(AutoDOS32 PRIVATE
    nlohmann_json::nlohmann_json
    comctl32
    shell32
    comdlg32
    ole32
)

# ── XP targeting ─────────────────────────────────────────────────────────────
# Build as 32-bit with XP-compatible settings
target_compile_definitions(AutoDOS32 PRIVATE
    WIN32_LEAN_AND_MEAN
    NOMINMAX
    _WIN32_WINNT=0x0501    # Windows XP
    WINVER=0x0501
    _WIN32_IE=0x0600
)

# Use v141_xp toolset for XP compatibility if available
# Set in Visual Studio: Project Properties → General → Platform Toolset → v141_xp
