# C++ Project Conventions Reference

This document describes the canonical C++ project structure and conventions used by the cpp-init skill.

## Directory Layout

```
project_root/
├── CMakeLists.txt          # Root CMake configuration
├── build.sh                # Build script (cmake wrapper)
├── run_tests.sh            # Test runner script
├── .clang-format           # C++ code formatting config
├── .cmake-format.yaml      # CMake code formatting config
├── .clang-tidy             # Static analysis config
├── .pre-commit-config.yaml # Pre-commit hooks
├── .gitignore              # Git ignore rules
├── .gitattributes          # Git attributes (line endings)
├── LICENSE                 # MIT License
├── README.md               # Project documentation
├── AGENTS.md               # Naming conventions & build guide for AI agents
├── src/                    # Source files
│   ├── main.cpp            # Entry point
│   └── *.hpp / *.cpp       # Library and implementation files
├── tests/                  # Test files
│   ├── CMakeLists.txt      # Test-specific CMake config
│   └── test_*.cpp          # One executable per test file
└── .github/                # GitHub templates
    ├── workflows/
    │   └── ci.yml          # CI: build + test + format + clang-tidy
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
- Export `compile_commands.json` for IDE/clangd/clang-tidy support
- Create a STATIC library (`{project}_lib`) that compiles all source files once, then links into executables
- Main executable linked against the static library
- `ENABLE_SANITIZERS` option (OFF by default) for ASan + UBSan
- `BUILD_TESTS` option (ON by default) for conditional test building
- Strict warnings: `-Wall -Wextra -Wpedantic -Werror -Wshadow -Wconversion`
- Debug: `-g -O0`, Release: `-O3`
- Google Test via `FetchContent` (v1.14.0) when `BUILD_TESTS` is ON — no system dependency

### tests/CMakeLists.txt

- One executable per `test_*.cpp` file
- Each test linked against the static library and `GTest::gtest_main`
- Uses `gtest_discover_tests()` to register each test with CTest
- Uses `file(GLOB ... CONFIGURE_DEPENDS ...)` to auto-discover test files

## Build Script (build.sh)

- Uses `set -euo pipefail` for strict error handling
- Default build type: Debug
- Skips configure if `build/CMakeCache.txt` already exists; delete `build/` to force re-configure
- Accepts build type as first argument: `./build.sh Release`
- Build directory: `build/`
- Generator: Ninja
- Compiler: g++ (configurable)
- Parallel build with `-j$(nproc)`

## Test Runner (run_tests.sh)

- Uses `set -euo pipefail` for strict error handling
- Uses `cmake -B build -S .` (same flags as `build.sh` Debug) when not yet configured
- Runs tests via `ctest --output-on-failure -j$(nproc)` for parallel execution
- Colored output (Red/Green/Yellow/Blue)
- Exit code 1 if any test fails, 0 if all pass
- Test framework: Google Test (via FetchContent, auto-downloaded during CMake configure)

## Test File Conventions

- File naming: `test_{module}.cpp` (e.g., `test_database.cpp`, `test_parser.cpp`)
- Each test file uses Google Test macros (`TEST`, `TEST_F`, `EXPECT_*`, `ASSERT_*`)
- Link with `GTest::gtest_main` to get an automatically generated `main()` entry point
- Include the module header being tested

```cpp
#include "module.hpp"
#include <gtest/gtest.h>

TEST(ModuleTest, BasicFunctionality) {
    auto result = function_under_test();
    ASSERT_TRUE(result.has_value());
    EXPECT_EQ(result->expected_property(), expected_value);
}
```

## Code Style (.clang-format)

- Based on LLVM style
- 4-space indentation, no tabs
- 120 column limit
- Attach braces (K&R style)
- Left-aligned pointers and references
- No bin-packing of parameters/arguments
- Include regrouping: C headers < C++ standard headers < project headers
- Empty line before access modifiers (public/private/protected)
- Operators at line start on break
- Template declarations always break
- Trailing comments aligned
- Compact nested namespaces

## CMake Style (.cmake-format.yaml)

- 120 column limit
- 4-space indentation
- Dangling parentheses (`)` on its own line)
- Lowercase commands, uppercase keywords
- No space between function name and `(`
- Space between control flow keywords and `(`
- No markup comments

## Static Analysis (.clang-tidy)

Enabled checks:
- `bugprone-*` (except `easily-swappable-parameters`)
- `modernize-*` (with `use-trailing-return-type`)
- `performance-*`
- `readability-*` (except `magic-numbers`, `identifier-naming`, `identifier-length`)
- `misc-*` (except `no-recursion`, `include-cleaner`)
- `portability-*`
- `cppcoreguidelines-pro-type-member-init`

Warnings are treated as errors. Header filter: `^(src|tests)/.*`

## Naming Conventions (AGENTS.md)

Identifier naming conventions are documented in `AGENTS.md` for AI agents to reference.
Naming is not enforced by clang-tidy (`readability-identifier-naming` is disabled).

| Category | Case | Prefix/Suffix |
|---|---|---|
| Classes | PascalCase | — |
| Structs | PascalCase | — |
| Functions | snake_case | — |
| Methods | snake_case | — |
| Variables | snake_case | — |
| Local variables | snake_case | — |
| Member variables | snake_case | trailing `_` |
| Constants | PascalCase | prefix `k` |
| Template parameters | PascalCase | — |

## Pre-commit Hooks (.pre-commit-config.yaml)

Uses the [pre-commit](https://pre-commit.com) framework. Hooks run on `git commit`:

1. **clang-format** — Auto-formats staged C++ files, re-stages changes
2. **cmake-format** — Auto-formats staged CMake files, re-stages changes
3. **clang-tidy** — Runs static analysis on staged C++ files, rejects commit on warnings

Requires `build/compile_commands.json` (run `./build.sh` first).

Setup:
```sh
pip install pre-commit
pre-commit install
```

## CI Pipeline (.github/workflows/ci.yml)

Three jobs:
1. **build-and-test**: Install GCC 13 + Ninja + CMake, configure, build, run `./run_tests.sh`
2. **format-check**: Install clang-format + cmake-format, check all files
3. **clang-tidy**: Install clang-tidy, configure CMake, run analysis on all source files

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
