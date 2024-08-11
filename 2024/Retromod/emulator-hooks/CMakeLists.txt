cmake_minimum_required(VERSION 3.10)

project(RetroGameEnhancer)

# Set C++ standard
set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED True)

# Add the emulator hooking source files
add_executable(RetroGameEnhancer emulator_hook.cpp)

# Include directories
include_directories(${CMAKE_SOURCE_DIR})

# Link libraries (if needed)
# target_link_libraries(RetroGameEnhancer some_library)

# Add custom commands or dependencies if necessary
