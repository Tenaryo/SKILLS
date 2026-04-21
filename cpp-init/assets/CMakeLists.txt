cmake_minimum_required(VERSION 3.21)

project({{PROJECT_NAME}} VERSION 1.0.0 LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 23)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_EXPORT_COMPILE_COMMANDS ON)

add_library({{LIB_NAME}} INTERFACE)
target_include_directories({{LIB_NAME}} INTERFACE ${CMAKE_SOURCE_DIR}/src)
target_compile_features({{LIB_NAME}} INTERFACE cxx_std_23)
target_compile_options({{LIB_NAME}} INTERFACE
    -Wall -Wextra -Wpedantic -Werror -Wshadow -Wconversion
    $<$<CONFIG:Debug>:-g -O0>
    $<$<CONFIG:Release>:-O3>
)

add_executable({{PROJECT_NAME}} src/main.cpp)
target_link_libraries({{PROJECT_NAME}} PRIVATE {{LIB_NAME}})

option(ENABLE_SANITIZERS "Enable Address and Undefined Behavior Sanitizers" OFF)

if(ENABLE_SANITIZERS)
    target_compile_options({{LIB_NAME}} INTERFACE -fsanitize=address,undefined -fno-omit-frame-pointer)
    target_link_options({{LIB_NAME}} INTERFACE -fsanitize=address,undefined)
endif()

option(BUILD_TESTS "Build tests" ON)
if(BUILD_TESTS)
    include(FetchContent)
    FetchContent_Declare(
        googletest
        GIT_REPOSITORY https://github.com/google/googletest.git
        GIT_TAG v1.14.0
    )
    set(gtest_force_shared_crt ON CACHE BOOL "" FORCE)
    FetchContent_MakeAvailable(googletest)
    enable_testing()
    add_subdirectory(tests)
endif()
