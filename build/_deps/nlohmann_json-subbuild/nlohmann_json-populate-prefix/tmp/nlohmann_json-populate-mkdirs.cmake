# Distributed under the OSI-approved BSD 3-Clause License.  See accompanying
# file LICENSE.rst or https://cmake.org/licensing for details.

cmake_minimum_required(VERSION ${CMAKE_VERSION}) # this file comes with cmake

# If CMAKE_DISABLE_SOURCE_CHANGES is set to true and the source directory is an
# existing directory in our source tree, calling file(MAKE_DIRECTORY) on it
# would cause a fatal error, even though it would be a no-op.
if(NOT EXISTS "C:/AutoDos/AutoDos32/AutoDOS32/AutoDOS32/build/_deps/nlohmann_json-src")
  file(MAKE_DIRECTORY "C:/AutoDos/AutoDos32/AutoDOS32/AutoDOS32/build/_deps/nlohmann_json-src")
endif()
file(MAKE_DIRECTORY
  "C:/AutoDos/AutoDos32/AutoDOS32/AutoDOS32/build/_deps/nlohmann_json-build"
  "C:/AutoDos/AutoDos32/AutoDOS32/AutoDOS32/build/_deps/nlohmann_json-subbuild/nlohmann_json-populate-prefix"
  "C:/AutoDos/AutoDos32/AutoDOS32/AutoDOS32/build/_deps/nlohmann_json-subbuild/nlohmann_json-populate-prefix/tmp"
  "C:/AutoDos/AutoDos32/AutoDOS32/AutoDOS32/build/_deps/nlohmann_json-subbuild/nlohmann_json-populate-prefix/src/nlohmann_json-populate-stamp"
  "C:/AutoDos/AutoDos32/AutoDOS32/AutoDOS32/build/_deps/nlohmann_json-subbuild/nlohmann_json-populate-prefix/src"
  "C:/AutoDos/AutoDos32/AutoDOS32/AutoDOS32/build/_deps/nlohmann_json-subbuild/nlohmann_json-populate-prefix/src/nlohmann_json-populate-stamp"
)

set(configSubDirs Debug)
foreach(subDir IN LISTS configSubDirs)
    file(MAKE_DIRECTORY "C:/AutoDos/AutoDos32/AutoDOS32/AutoDOS32/build/_deps/nlohmann_json-subbuild/nlohmann_json-populate-prefix/src/nlohmann_json-populate-stamp/${subDir}")
endforeach()
if(cfgdir)
  file(MAKE_DIRECTORY "C:/AutoDos/AutoDos32/AutoDOS32/AutoDOS32/build/_deps/nlohmann_json-subbuild/nlohmann_json-populate-prefix/src/nlohmann_json-populate-stamp${cfgdir}") # cfgdir has leading slash
endif()
