# C++ Project Conventions Reference

This document describes the canonical C++ project structure and conventions used by the cpp-init skill.

## Directory Layout

```
project_root/
├── CMakeLists.txt          # Root CMake configuration
├── build.sh                # Build script (cmake wrapper)
├── run_tests.sh            # Test runner script
├── .clang-format           # Code formatting config
├── .gitignore              # Git ignore rules
├── .gitattributes          # Git attributes (line endings)
├── LICENSE                 # MIT License
├── README.md               # Project documentation
├── src/                    # Source files
│   ├── main.cpp            # Entry point
│   └── *.hpp / *.cpp       # Library and implementation files
├── tests/                  # Test files
│   ├── CMakeLists.txt      # Test-specific CMake config
│   └── test_*.cpp          # One executable per test file
└── .github/                # GitHub templates
    ├── workflows/
    │   └── ci.yml          # CI: build + test + format check
    ├── PULL_REQUEST_TEMPLATE.md
    └── ISSUE_TEMPLATE/
        ├── bug_report.yml
        ├── config.yml
        ├── feature_request.yml
        └── question.yml
```

## CMake Conventions

### Root CMakeLists.txt

- Minimum version: 3.21
- C++ standard: 23 (configurable)
- Build system generator: Ninja
- Export `compile_commands.json` for IDE/clangd support
- Create an INTERFACE library (`{project}_core`) for header-only or shared compile options
- Main executable linked against the core library
- `ENABLE_SANITIZERS` option (OFF by default) for ASan + UBSan
- `BUILD_TESTS` option (ON by default) for conditional test building
- Strict warnings: `-Wall -Wextra -Wpedantic -Werror -Wshadow -Wconversion`
- Debug: `-g -O0`, Release: `-O3`

### tests/CMakeLists.txt

- One executable per `test_*.cpp` file
- Each test linked against the core library
- `-UNDEBUG` flag to ensure `assert()` works in all build modes
- Uses `file(GLOB ...)` to auto-discover test files

## Build Script (build.sh)

- Uses `set -euo pipefail` for strict error handling
- Default build type: Debug
- Accepts build type as first argument: `./build.sh Release`
- Build directory: `build/`
- Generator: Ninja
- Compiler: g++ (configurable)
- Parallel build with `-j$(nproc)`

## Test Runner (run_tests.sh)

- Uses `set -euo pipefail` for strict error handling
- Auto-configures CMake if not already configured
- Discovers all `tests/test_*.cpp` files and their corresponding executables
- Runs each test independently
- Colored output (Red/Green/Yellow/Blue)
- Summary with pass/fail counts
- Exit code 1 if any test fails, 0 if all pass
- No external test framework dependency (uses raw `assert()`)

## Test File Conventions

- File naming: `test_{module}.cpp` (e.g., `test_database.cpp`, `test_parser.cpp`)
- Each test file is a standalone executable with its own `main()`
- Use `assert()` for assertions (no framework dependency)
- Return `EXIT_SUCCESS` on pass, assertion failure causes abort
- Include the module header being tested

```cpp
#include "module.hpp"
#include <cassert>
#include <cstdlib>

auto main() -> int {
    // Test cases in scoped blocks
    {
        auto result = function_under_test();
        assert(result.has_value());
        assert(result->expected_property() == expected_value);
    }

    return EXIT_SUCCESS;
}
```

## Code Style (.clang-format)

- Based on LLVM style
- 4-space indentation, no tabs
- 100 column limit
- Attach braces (`K&R style`)
- Left-aligned pointers and references
- No bin-packing of parameters/arguments
- Sort includes case-sensitively

## CI Pipeline (.github/workflows/ci.yml)

Two jobs:
1. **build-and-test**: Install GCC 13 + Ninja + CMake, configure, build, run `./run_tests.sh`
2. **format-check**: Install clang-format, check all `.cpp`/`.hpp` files in `src/` and `tests/`

Triggers: push to main/master, pull requests to main/master.

## Commit Message Convention

Follow conventional commits:
- `feat:` new feature
- `fix:` bug fix
- `refactor:` code restructuring
- `test:` adding/updating tests
- `docs:` documentation changes
- `build:` build system changes
- `ci:` CI configuration changes
- `style:` formatting (no code change)
- `chore:` maintenance tasks

## Git Conventions

- `.gitattributes`: `* text=auto` for consistent line endings
- `.gitignore`: Ignores build/, CMake artifacts, IDE files, compiled objects, OS files
