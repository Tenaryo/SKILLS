cmake_minimum_required(VERSION 3.21)

project({{PROJECT_NAME}} VERSION 1.0.0 LANGUAGES CXX)

set(CMAKE_EXPORT_COMPILE_COMMANDS ON)

file(GLOB_RECURSE LIB_SOURCES CONFIGURE_DEPENDS "${CMAKE_SOURCE_DIR}/src/*.cpp")
list(FILTER LIB_SOURCES EXCLUDE REGEX "main\\.cpp$")

add_library({{LIB_NAME}} STATIC ${LIB_SOURCES})
target_include_directories({{LIB_NAME}} PUBLIC ${CMAKE_SOURCE_DIR}/src)
add_library({{PROJECT_NAME}}::lib ALIAS {{LIB_NAME}})
target_compile_features({{LIB_NAME}} PUBLIC cxx_std_23)
target_compile_options({{LIB_NAME}} PUBLIC
    -Wall -Wextra -Wpedantic -Werror -Wshadow -Wconversion
    $<$<CONFIG:Debug>:-g -O0>
    $<$<CONFIG:Release>:-O3>
)

add_executable({{PROJECT_NAME}} src/main.cpp)
target_link_libraries({{PROJECT_NAME}} PRIVATE {{LIB_NAME}})

option(ENABLE_SANITIZERS "Enable Address and Undefined Behavior Sanitizers" OFF)

if(ENABLE_SANITIZERS)
    target_compile_options({{LIB_NAME}} PUBLIC -fsanitize=address,undefined -fno-omit-frame-pointer)
    target_link_options({{LIB_NAME}} PUBLIC -fsanitize=address,undefined)
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
    include(GoogleTest)
    enable_testing()
    add_subdirectory(tests)
endif()
